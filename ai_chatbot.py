import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
import qdrant_client
from qdrant_client.models import Distance, VectorParams, PointStruct
import openai
import os
from typing import List, Dict, Tuple
import PyPDF2
import docx
from pathlib import Path
import uuid
from dotenv import load_dotenv
import os
import requests
import config
from tqdm import tqdm
import cohere


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

class AIDocumentChatbot:
    def __init__(self, openai_api_key: str, collection_name: str = "documents"):
        """
        Initialize the AI chatbot with vector search and OpenAI integration.
        
        Args:
            openai_api_key: Your OpenAI API key
            collection_name: Name for the Qdrant collection
        """
        # Initialize OpenAI
        openai.api_key = openai_api_key
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        # Initialize embedding model
        print("Loading embedding model...")
        import requests
        self.jina_api_key = os.getenv("JINA_API_KEY")

        # Always load local model as fallback
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)

        if self.jina_api_key:
            self.use_jina = True
            self.embedding_dim = 768
            print("Using JinaAI embeddings (with local fallback)")
        else:
            self.use_jina = False
            self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
            print(f"Using {config.EMBEDDING_MODEL} (dimension: {self.embedding_dim})")
        
        # Initialize Cohere model
        print("Loading Cohere reranker...")
        cohere_key = os.getenv("COHERE_API_KEY")
        if cohere_key:
            self.cohere_client = cohere.Client(cohere_key)
            self.use_cohere = True
            print(f"Using cohere reranker")
        else:
            print("Cohere API key not found, using CrossEncoder fallback")
            from sentence_transformers import CrossEncoder
            self.reranker = CrossEncoder(config.RERANKER_MODEL)
            self.use_cohere = False
            print(f"Using {config.RERANKER}") # type: ignore
        
        # Initialize Qdrant client (in-memory for simplicity)
        print("Initializing vector database...")
        self.qdrant_client = qdrant_client.QdrantClient(":memory:")
        self.collection_name = collection_name
        
        # Create collection with cosine similarity
        self.qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.embedding_dim, # type: ignore
                distance=Distance.COSINE
            )
        )
        
        # Store metadata for mapping indices back
        self.metadata_store = {}
        self.point_id_counter = 0
        
        print("✓ Chatbot initialized successfully!")


    def get_jina_embeddings(self, texts):
        """Get embeddings from JinaAI API"""
        url = 'https://api.jina.ai/v1/embeddings'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.jina_api_key}'
        }

        data = {
            'model': 'jina-embeddings-v2-base-en',
            'input': texts if isinstance(texts, list) else [texts]
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        embeddings = [item['embedding'] for item in result['data']]

        return embeddings[0] if isinstance(texts, str) else embeddings

    def _get_jina_embeddings_with_progress(self, texts):
        import time
        
        url = 'https://api.jina.ai/v1/embeddings'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.jina_api_key}'
        }
        
        batch_size = 50
        all_embeddings = []
        
        # Progress bar for batches
        for i in tqdm(range(0, len(texts), batch_size), 
                    desc="  JinaAI API", 
                    unit="batch",
                    leave=False):
            batch = texts[i:i + batch_size]
            
            data = {
                'model': 'jina-embeddings-v2-base-en',
                'input': batch
            }
            
            # Retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.post(url, headers=headers, json=data, timeout=30)
                    response.raise_for_status()
                    
                    result = response.json()
                    batch_embeddings = [item['embedding'] for item in result['data']]
                    all_embeddings.extend(batch_embeddings)
                    
                    # Small delay
                    if i + batch_size < len(texts):
                        time.sleep(0.3)
                    
                    break
                    
                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        time.sleep((attempt + 1) * 2)
                    else:
                        # Fallback
                        if not hasattr(self, 'embedding_model'):
                            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
                        batch_embeddings = self.embedding_model.encode(batch, show_progress_bar=False)
                        all_embeddings.extend([emb.tolist() for emb in batch_embeddings])
        
        return all_embeddings


    
    def extract_text_from_file(self, file_path: str) -> List[Dict[str, any]]: # type: ignore
        """
        Extract text from various file formats and chunk it.
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of chunks with metadata
        """
        file_path = Path(file_path) # type: ignore
        text = ""
        
        # Extract text based on file type
        if file_path.suffix.lower() == '.pdf': # type: ignore
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page.extract_text()
        
        elif file_path.suffix.lower() in ['.docx', '.doc']: # type: ignore
            doc = docx.Document(file_path)
            for para_num, para in enumerate(doc.paragraphs):
                text += para.text + "\n"
        
        elif file_path.suffix.lower() == '.txt': # type: ignore
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}") # type: ignore
        
        # Chunk the text into sentences/paragraphs
        chunks = self._chunk_text(text, file_path.name) # type: ignore
        
        return chunks
    
    def _chunk_text(self, text: str, filename: str, chunk_size: int = None): # type: ignore
        if chunk_size is None:
            chunk_size = config.CHUNK_SIZE

        """
        Split text into manageable chunks with metadata.
        
        Args:
            text: The text to chunk
            filename: Name of the source file
            chunk_size: Target size for each chunk in characters
            
        Returns:
            List of dictionaries containing chunk text and metadata
        """
        chunks = []
        
        # Split by paragraphs first
        paragraphs = text.split('\n')
        
        current_chunk = ""
        chunk_id = 0
        page_num = 1
        
        for para in paragraphs:
            # Track page numbers
            if "--- Page" in para:
                try:
                    page_num = int(para.split("Page")[1].split("---")[0].strip())
                    continue
                except:
                    pass
            
            para = para.strip()
            if not para:
                continue
            
            # If adding this paragraph would exceed chunk size, save current chunk
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                chunks.append({
                    'text': current_chunk.strip(),
                    'metadata': {
                        'filename': filename,
                        'chunk_id': chunk_id,
                        'page': page_num
                    }
                })
                current_chunk = para
                chunk_id += 1
            else:
                current_chunk += " " + para if current_chunk else para
        
        # Add the last chunk
        if current_chunk:
            chunks.append({
                'text': current_chunk.strip(),
                'metadata': {
                    'filename': filename,
                    'chunk_id': chunk_id,
                    'page': page_num
                }
            })
        
        return chunks
    
    def add_documents(self, file_paths: List[str]):
        """
        Process and add multiple documents to the vector database.
        
        Args:
            file_paths: List of paths to documents
        """
        print(f"\nProcessing {len(file_paths)} document(s)...")
        
        all_points = []
        
        for file_path in tqdm(file_paths, desc="Loading files", unit="file"):
            
            # Extract and chunk text
            chunks = self.extract_text_from_file(file_path)
            
            # Generate embeddings for all chunks
            texts = [chunk['text'] for chunk in chunks]

            print(f" {file_path}: {len(chunks)} chunks, generating embeddings...")
            
            if self.use_jina:
                embeddings = self._get_jina_embeddings_with_progress(texts)
            else:
                embeddings = []
                batch_size = 32
                for i in tqdm(range(0, len(texts), batch_size),
                        desc=f" Embedding",
                        unit="batch",
                        leave=False):
                    batch = texts[i:i + batch_size]
                    batch_embeddings = self.embedding_model.encode(batch, show_progress_bar=False)
                    embeddings.extend(batch_embeddings)
            
            # Create points for Qdrant
            for chunk, embedding in tqdm(zip(chunks, embeddings),
                                        total=len(chunks),
                                        desc=f" Creating vectors",
                                        unit="chunk",
                                        leave=False):
                point_id = self.point_id_counter

                # Store metadata
                self.metadata_store[point_id] = chunk['metadata']

                # Convert embedding to list if it's not already
                if hasattr(embedding, 'tolist'):
                    vector = embedding.tolist()
                else:
                    vector = embedding
                

                # Create point
                point = PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        'text': chunk['text'],
                        'filename': chunk['metadata']['filename'],
                        'chunk_id': chunk['metadata']['chunk_id'],
                        'page': chunk['metadata']['page']
                    }
                )
                all_points.append(point)

                self.point_id_counter += 1
        
        # Upload to Qdrant
        print(f"\nUploading {len(all_points)} vectors to database...")
        
        batch_size = 100
        for i in tqdm(range(0, len(all_points), batch_size),
                    desc="Uploading",
                    unit="batch"):
            batch = all_points[i:i + batch_size]
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
        print("✓ All documents processed and indexed!\n")
    
    def search_similar_chunks(self, query: str, top_k: int = 20) -> List[Dict]:
        """
        Step 1-3: Convert query to vector, search database, and return top similar chunks.
        
        Args:
            query: User's search query
            top_k: Number of similar chunks to retrieve
            
        Returns:
            List of similar chunks with metadata

        """
        # Step 1: Convert query to vector

        print(f"[SEARCH DEBUG] Searching for: '{query[:50]}...'")
        print(f"[SEARCH DEBUG] Collection: {self.collection_name}")
        print(f"[SEARCH DEBUG] Total points in metadata: {len(self.metadata_store)}")

        if self.use_jina:
            query_vector = self.get_jina_embeddings(query)
        else:
            query_vector = self.embedding_model.encode(query)
        
        # Step 2-3: Search for similar vectors and map back to metadata
        # Convert to a list if needed
        if hasattr(query_vector, 'tolist'):
            query_vector_list = query_vector.tolist() # type: ignore
        else:
            query_vector_list = query_vector

        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector_list, # type: ignore
            limit=top_k
        )

        print(f"[SEARCH DEBUG] Found {len(search_results)} results")
        
        # Extract results with metadata
        results = []
        for result in search_results:
            if result.payload:
                results.append({
                    'id': result.id,
                    'score': result.score,
                    'text': result.payload['text'],
                    'metadata': {
                        'filename': result.payload['filename'],
                        'chunk_id': result.payload['chunk_id'],
                        'page': result.payload['page']
                    }
                })
        return results
    
    def rerank_results(self, query: str, results: List[Dict], top_n: int = 5) -> List[Dict]:

        if self.use_cohere:
            # Use Cohere reranker
            documents = [result['text'] for result in results]
            
            # Call Cohere rerank API
            rerank_response = self.cohere_client.rerank(
                model='rerank-english-v3.0',  # or 'rerank-multilingual-v3.0'
                query=query,
                documents=documents,
                top_n=top_n
            )
            
            # Map back to original results
            reranked = []
            for item in rerank_response.results:
                original_result = results[item.index]
                original_result['rerank_score'] = item.relevance_score
                reranked.append(original_result)
            
            return reranked
        else:
            # Fallback to original cross-encoder
            pairs = [(query, result['text']) for result in results]
            rerank_scores = self.reranker.predict(pairs)
            
            for result, score in zip(results, rerank_scores):
                result['rerank_score'] = float(score)
            
            reranked = sorted(results, key=lambda x: x['rerank_score'], reverse=True)
            return reranked[:top_n]

    
    def get_answer_from_ai(self, query: str, context_chunks: List[Dict], model: str = "gpt-4o-mini", provider: str = "openai") -> str:
        """
        Step 5: Pass the top pages/chunks to AI API to generate an answer.
        
        Args:
            query: User's question
            context_chunks: Top relevant chunks after reranking
            model: AI model to use
            provider: Provider (openai, ollama, anthropic)
            
        Returns:
            AI-generated answer
        """
        # Prepare context from chunks
        context = ""
        for i, chunk in enumerate(context_chunks, 1):
            context += f"\n--- Source {i} (File: {chunk['metadata']['filename']}, Page: {chunk['metadata']['page']}) ---\n"
            context += chunk['text'] + "\n"
        
        # Create prompt
        system_prompt = """You are a helpful AI assistant that answers questions based on the provided document context. 

IMPORTANT FORMATTING RULES:
- Always cite which source and page number you're referring to when answering
- When presenting data from tables, format it cleanly with proper spacing
- If data contains numbers, present them in a clear, organized manner
- Use bullet points or numbered lists for multiple data points
- Add line breaks between different pieces of information
- If the answer cannot be found in the provided context, say so clearly

EXAMPLE OF GOOD FORMATTING:
Employee data appears on the following pages:
- Page 5 - Overview: 026 employees
- Page 28 - Training participation: 94-95%
- Page 34 - International deployment: 960 employees
- Page 185 - Contract employees: 93-114 persons"""
        
        user_prompt = f"""Context from documents:
{context}

Question: {query}

IMPORTANT INSTRUCTIONS:
- If the question asks about "how many pages" or "which pages", examine ALL provided sources carefully
- List EVERY unique page number where the information appears
- Do not miss any pages from the sources provided
- Be comprehensive and thorough

Please provide a detailed answer based on the context above. Cite your sources with file names and page numbers."""
        
        # Call appropriate API based on provider
        if provider == "openai":
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content # type: ignore
        
        elif provider == "ollama":
            # Call Ollama API
            import requests
            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            response = requests.post(
                f"{ollama_url}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        
        elif provider == "anthropic":
            # Call Anthropic API (requires anthropic library)
            try:
                from anthropic import Anthropic
                anthropic_key = os.getenv("ANTHROPIC_API_KEY")
                if not anthropic_key:
                    return "Error: Anthropic API key not configured"
                
                anthropic_client = Anthropic(api_key=anthropic_key)
                response = anthropic_client.messages.create(
                    model=model,
                    max_tokens=1500,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.content[0].text
            except Exception as e:
                return f"Error calling Anthropic: {str(e)}"
        
        else:
            return f"Error: Unsupported provider '{provider}'"
    
    # Keep the old method name for backwards compatibility
    def get_answer_from_openai(self, query: str, context_chunks: List[Dict]) -> str:
        """Backwards compatibility wrapper"""
        return self.get_answer_from_ai(query, context_chunks, model="gpt-4o-mini", provider="openai")
    
    def query(self, question: str, num_candidates: int = None, num_rerank: int = None, verbose: bool = True, model: str = None, provider: str = 'openai'): # type: ignore
        if num_candidates is None:
            num_candidates = config.NUM_CANDIDATES
        if num_rerank is None:
            num_rerank = config.NUM_RERANK
        if model is None:
            model = "gpt-4o-mini"

        
        """
        Complete query pipeline: search, rerank, and get AI answer.
        
        Args:
            question: User's question
            num_candidates: Number of candidates to retrieve from vector search
            num_rerank: Number of top results after reranking
            verbose: Whether to print intermediate steps
            model: AI model to use for generating answer
            provider: Provider of the model (openai, ollama, anthropic)
            
        Returns:
            Dictionary containing answer and metadata
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"Query: {question}")
            print(f"{'='*60}\n")
        
        # Step 1-3: Vector search
        if verbose:
            print(f"Step 1-3: Searching vector database...")
        search_results = self.search_similar_chunks(question, top_k=num_candidates)
        if verbose:
            print(f"  → Found {len(search_results)} similar chunks\n")
        
        # Step 4: Reranking
        if verbose:
            print(f"Step 4: Reranking results...")
        reranked_results = self.rerank_results(question, search_results, top_n=num_rerank)
        if verbose:
            print(f"  → Top {len(reranked_results)} chunks after reranking\n")
            for i, result in enumerate(reranked_results, 1):
                print(f"  {i}. [Score: {result['rerank_score']:.3f}] {result['metadata']['filename']} (Page {result['metadata']['page']})")
            print()
        
        # Step 5: Get answer from AI model
        if verbose:
            print(f"Step 5: Generating answer with {model}...\n")
        answer = self.get_answer_from_ai(question, reranked_results, model=model, provider=provider)
        
        return {
            'answer': answer,
            'sources': reranked_results,
            'num_candidates': len(search_results),
            'num_reranked': len(reranked_results)
        }


# Example usage
if __name__ == "__main__":
    # Initialize chatbot
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    
    chatbot = AIDocumentChatbot(
        openai_api_key=OPENAI_API_KEY,
        collection_name="my_documents"
    )
    
    # Add documents
    # chatbot.add_documents([
    #     "document1.pdf",
    #     "document2.txt",
    #     "document3.docx"
    # ])
    
    # Query the chatbot
    # result = chatbot.query("What are the main findings?")
    # print(result['answer'])