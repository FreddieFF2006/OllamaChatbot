"""
AI Chatbot with Ollama, OpenAI, Anthropic Integration and Document Embedding
Supports local Ollama models, OpenAI ChatGPT, Anthropic Claude, and Document Q&A
"""

from flask import Flask, render_template, request, jsonify, Response, stream_with_context, session
import requests
import json
from typing import Generator
import os
from dotenv import load_dotenv
import secrets


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
PPT_SERVICE_URL = "http://localhost:5001"

# Ollama API configuration
OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')

# OpenAI API configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# Anthropic API configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# Try to import OpenAI
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
    OPENAI_AVAILABLE = bool(OPENAI_API_KEY)
except ImportError:
    openai_client = None
    OPENAI_AVAILABLE = False

# Try to import Anthropic
try:
    from anthropic import Anthropic
    if ANTHROPIC_API_KEY:
        try:
            anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
            ANTHROPIC_AVAILABLE = True
        except (TypeError, Exception) as e:
            print(f"⚠️ Warning: Could not initialize Anthropic client: {e}")
            print("   Anthropic models will not be available.")
            anthropic_client = None
            ANTHROPIC_AVAILABLE = False
    else:
        anthropic_client = None
        ANTHROPIC_AVAILABLE = False
except ImportError:
    anthropic_client = None
    ANTHROPIC_AVAILABLE = False

# Try to import embedding dependencies
try:
    from ai_chatbot import AIDocumentChatbot
    import config
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False
    print("⚠️ Embedding dependencies not available. Install requirements for embedding feature.")

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url
    
    def get_models(self) -> dict:
        """Fetch all available models from Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "models": []}
    
    def chat_stream(self, model: str, messages: list, temperature: float = 0.7) -> Generator:
        """Stream chat responses from Ollama"""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature
            }
        }
        
        try:
            response = requests.post(url, json=payload, stream=True, timeout=60)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "message" in chunk:
                            content = chunk["message"].get("content", "")
                            if content:
                                yield f"data: {json.dumps({'content': content})}\n\n"
                        
                        if chunk.get("done", False):
                            yield f"data: {json.dumps({'done': True})}\n\n"
                    except json.JSONDecodeError:
                        continue
                        
        except requests.exceptions.RequestException as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    def generate(self, model: str, prompt: str, temperature: float = 0.7) -> Generator:
        """Generate text completion from Ollama (non-chat mode)"""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature
            }
        }
        
        try:
            response = requests.post(url, json=payload, stream=True, timeout=60)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        content = chunk.get("response", "")
                        if content:
                            yield f"data: {json.dumps({'content': content})}\n\n"
                        
                        if chunk.get("done", False):
                            yield f"data: {json.dumps({'done': True})}\n\n"
                    except json.JSONDecodeError:
                        continue
                        
        except requests.exceptions.RequestException as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"


class OpenAIClient:
    """Client for interacting with OpenAI API"""
    
    def __init__(self):
        self.client = openai_client
        self.available_models = [
            "gpt-4-turbo-preview",
            "gpt-4",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]
    
    def get_models(self) -> list:
        """Return available OpenAI models"""
        if not self.client:
            return []
        return [{"name": model, "provider": "openai"} for model in self.available_models]
    
    def chat_stream(self, model: str, messages: list, temperature: float = 0.7) -> Generator:
        """Stream chat responses from OpenAI"""
        if not self.client:
            yield f"data: {json.dumps({'error': 'OpenAI API key not configured'})}\n\n"
            return
        
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    yield f"data: {json.dumps({'content': content})}\n\n"
            
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    def generate(self, model: str, prompt: str, temperature: float = 0.7) -> Generator:
        """Generate text completion from OpenAI"""
        messages = [{"role": "user", "content": prompt}]
        return self.chat_stream(model, messages, temperature)


class AnthropicClient:
    """Client for interacting with Anthropic Claude API"""
    
    def __init__(self):
        self.client = anthropic_client
        self.available_models = [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
    
    def get_models(self) -> list:
        """Return available Anthropic Claude models"""
        if not self.client:
            return []
        return [{"name": model, "provider": "anthropic"} for model in self.available_models]
    
    def chat_stream(self, model: str, messages: list, temperature: float = 0.7) -> Generator:
        """Stream chat responses from Claude"""
        if not self.client:
            yield f"data: {json.dumps({'error': 'Anthropic API key not configured'})}\n\n"
            return
        
        try:
            # Convert messages to Claude format if needed
            claude_messages = []
            system_message = None
            
            for msg in messages:
                if msg.get("role") == "system":
                    system_message = msg.get("content")
                else:
                    claude_messages.append({
                        "role": msg.get("role"),
                        "content": msg.get("content")
                    })
            
            # Create stream request
            stream_params = {
                "model": model,
                "messages": claude_messages,
                "temperature": temperature,
                "max_tokens": 4096
            }
            
            if system_message:
                stream_params["system"] = system_message
            
            # Use the streaming context manager correctly
            with self.client.messages.stream(**stream_params) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'content': text})}\n\n"
            
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    def generate(self, model: str, prompt: str, temperature: float = 0.7) -> Generator:
        """Generate text completion from Claude"""
        messages = [{"role": "user", "content": prompt}]
        return self.chat_stream(model, messages, temperature)

# Initialize clients
ollama = OllamaClient()
openai = OpenAIClient() if OPENAI_AVAILABLE else None
anthropic = AnthropicClient() if ANTHROPIC_AVAILABLE else None

# Store chatbot instances per session
chatbot_instances = {}

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/embedding')
def embedding():
    """Render the document embedding interface"""
    if not EMBEDDING_AVAILABLE:
        return "Embedding feature not available. Please install required dependencies.", 503
    return render_template('embedding.html')

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get all available models from Ollama, OpenAI, and Anthropic"""
    all_models = []
    
    # Get Ollama models
    models_data = ollama.get_models()
    
    if "error" not in models_data and "models" in models_data:
        for model in models_data["models"]:
            all_models.append({
                "name": model.get("name", "unknown"),
                "size": model.get("size", 0),
                "modified_at": model.get("modified_at", ""),
                "digest": model.get("digest", ""),
                "provider": "ollama"
            })
    
    # Get OpenAI models
    if openai:
        openai_models = openai.get_models()
        all_models.extend(openai_models)
    
    # Get Anthropic Claude models
    if anthropic:
        anthropic_models = anthropic.get_models()
        all_models.extend(anthropic_models)
    
    return jsonify({
        "success": True,
        "models": all_models,
        "openai_available": OPENAI_AVAILABLE,
        "anthropic_available": ANTHROPIC_AVAILABLE
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with streaming response"""
    data = request.json
    model = data.get('model', 'llama2')
    messages = data.get('messages', [])
    temperature = data.get('temperature', 0.7)
    provider = data.get('provider', 'ollama')
    
    if not messages:
        return jsonify({"error": "No messages provided"}), 400
    
    # Route to correct provider
    if provider == 'openai':
        if not openai:
            return jsonify({"error": "OpenAI not configured"}), 400
        stream = openai.chat_stream(model, messages, temperature)
    elif provider == 'anthropic':
        if not anthropic:
            return jsonify({"error": "Anthropic not configured"}), 400
        stream = anthropic.chat_stream(model, messages, temperature)
    else:
        stream = ollama.chat_stream(model, messages, temperature)
    
    return Response(
        stream_with_context(stream),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/api/generate', methods=['POST'])
def generate():
    """Handle text generation requests with streaming response"""
    data = request.json
    model = data.get('model', 'llama2')
    prompt = data.get('prompt', '')
    temperature = data.get('temperature', 0.7)
    provider = data.get('provider', 'ollama')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    # Route to correct provider
    if provider == 'openai':
        if not openai:
            return jsonify({"error": "OpenAI not configured"}), 400
        stream = openai.generate(model, prompt, temperature)
    elif provider == 'anthropic':
        if not anthropic:
            return jsonify({"error": "Anthropic not configured"}), 400
        stream = anthropic.generate(model, prompt, temperature)
    else:
        stream = ollama.generate(model, prompt, temperature)
    
    return Response(
        stream_with_context(stream),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/api/health', methods=['GET'])
def health():
    """Check if Ollama server is running"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        response.raise_for_status()
        return jsonify({"status": "healthy", "ollama_connected": True})
    except requests.exceptions.RequestException:
        return jsonify({"status": "unhealthy", "ollama_connected": False}), 503

# ============================================
# EMBEDDING ROUTES
# ============================================

@app.route('/api/embedding/status', methods=['GET'])
def embedding_status():
    """Check if embedding feature is available"""
    return jsonify({
        "available": EMBEDDING_AVAILABLE,
        "openai_configured": bool(OPENAI_API_KEY)
    })


@app.route('/api/embedding/init', methods=['POST'])
def init_embedding():
    """Initialize the embedding chatbot"""
    if not EMBEDDING_AVAILABLE:
        return jsonify({"error": "Embedding feature not available"}), 503
    
    if not OPENAI_API_KEY:
        return jsonify({"error": "OpenAI API key not configured"}), 400
    
    try:
        # Create a unique session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = secrets.token_hex(8)
        
        session_id = session['session_id']
        
        # Initialize chatbot instance
        chatbot_instances[session_id] = {
            'chatbot': AIDocumentChatbot(
                openai_api_key=OPENAI_API_KEY,
                collection_name=f"docs_{session_id}"
            ),
            'documents': []
        }
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Chatbot initialized successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/embedding/upload', methods=['POST'])
def upload_documents():
    """Upload and process documents for embedding"""
    if not EMBEDDING_AVAILABLE:
        return jsonify({"error": "Embedding feature not available"}), 503
    
    session_id = session.get('session_id')
    if not session_id or session_id not in chatbot_instances:
        return jsonify({"error": "Chatbot not initialized. Please initialize first."}), 400
    
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400
    
    files = request.files.getlist('files')
    
    if not files:
        return jsonify({"error": "No files selected"}), 400
    
    try:
        chatbot = chatbot_instances[session_id]['chatbot']
        processed_files = []
        
        for file in files:
            if file.filename:
                # Save file temporarily and process
                file_path = f"/tmp/{file.filename}"
                file.save(file_path)
                chatbot.load_document(file_path)
                processed_files.append(file.filename)
        
        return jsonify({
            "success": True,
            "files": processed_files,
            "message": f"Processed {len(processed_files)} document(s)"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/embedding/query', methods=['POST'])
def query_documents():
    """Query the document embedding system"""
    if not EMBEDDING_AVAILABLE:
        return jsonify({"error": "Embedding feature not available"}), 503
    
    session_id = session.get('session_id')
    if not session_id or session_id not in chatbot_instances:
        return jsonify({"error": "Chatbot not initialized or no documents loaded"}), 400
    
    data = request.json
    question = data.get('question', '')
    model = data.get('model', 'gpt-4o-mini')
    provider = data.get('provider', 'openai')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        chatbot = chatbot_instances[session_id]['chatbot']
        
        # Import config if needed
        import config
        
        # Query the chatbot - returns tuple of (answer, sources)
        result = chatbot.query(
            question=question,
            model=model,
            num_candidates=config.NUM_CANDIDATES,
            num_rerank=config.NUM_RERANK,
            verbose=False,
            provider=provider
        )
        
        # Unpack the result tuple
        answer = result['answer']
        sources = result['sources']
        
        # Format sources for response
        formatted_sources = [
            {
                "filename": s.get("filename", "Unknown"),
                "page": s.get("page", 0),
                "chunk_id": s.get("chunk_id", 0),
                "score": s.get("score", 0)
            }
            for s in sources
        ]
        
        return jsonify({
            "success": True,
            "answer": answer,
            "sources": formatted_sources
        })
    except Exception as e:
        import traceback
        print(f"ERROR in query_documents: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/embedding/reset', methods=['POST'])
def reset_embedding():
    """Reset the embedding session"""
    session_id = session.get('session_id')
    
    if session_id and session_id in chatbot_instances:
        # Clean up resources
        del chatbot_instances[session_id]
        
        # Clean up uploaded files if any
        upload_folder = f"/tmp/uploads_{session_id}"
        if os.path.exists(upload_folder):
            import shutil
            shutil.rmtree(upload_folder)
    
    session.clear()
    return jsonify({"success": True, "message": "Session reset successfully"})


# ============================================
# PPT EXTRACTION INTEGRATION ROUTES
# ============================================

@app.route('/api/ppt/check-service', methods=['GET'])
def check_ppt_service():
    """Check if PPT extraction service is available"""
    try:
        response = requests.get(f"{PPT_SERVICE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "available": True,
                "service_info": data
            })
        else:
            return jsonify({"available": False, "error": "Service unavailable"})
    except requests.exceptions.RequestException as e:
        return jsonify({"available": False, "error": str(e)})


@app.route('/api/ppt/extract', methods=['POST'])
def extract_ppt_via_service():
    """Forward PPT file to extraction service and get JSON back"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Get form data
        client = request.form.get('client', 'openai')
        model = request.form.get('model', 'gpt-4o-mini')
        api_key = request.form.get('api_key', '')
        instructions = request.form.get('instructions', '')
        rate_limit = request.form.get('rate_limit', '60')
        
        if not api_key:
            return jsonify({"error": "API key is required"}), 400
        
        # Prepare the file and form data for forwarding
        files = {'file': (file.filename, file.stream, file.content_type)}
        form_data = {
            'client': client,
            'model': model,
            'api_key': api_key,
            'instructions': instructions,
            'rate_limit': rate_limit
        }
        
        # Forward to PPT extraction service
        response = requests.post(
            f"{PPT_SERVICE_URL}/api/extract",
            files=files,
            data=form_data,
            timeout=600  # 10 minutes timeout for large files
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {"error": response.text}
            return jsonify(error_data), response.status_code
    
    except requests.exceptions.Timeout:
        return jsonify({"error": "PPT extraction timed out. File may be too large."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to communicate with PPT service: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def add_text_chunks_to_chatbot(chatbot, text_chunks, source_name="PowerPoint"):
    """Helper function to add pre-chunked text to the chatbot"""
    from qdrant_client.models import PointStruct
    
    print(f"[DEBUG] Starting add_text_chunks_to_chatbot with {len(text_chunks)} chunks")
    
    # Prepare chunks in the format expected by the embedding system
    formatted_chunks = []
    for i, text in enumerate(text_chunks):
        formatted_chunks.append({
            'text': text,
            'metadata': {
                'filename': source_name,
                'page': i + 1,
                'chunk_id': i
            }
        })
    
    print(f"[DEBUG] Formatted {len(formatted_chunks)} chunks")
    
    # Generate embeddings
    texts = [chunk['text'] for chunk in formatted_chunks]
    
    print(f"[DEBUG] Generating embeddings for {len(texts)} chunks using {'JinaAI' if chatbot.use_jina else 'local model'}...")
    
    if chatbot.use_jina:
        embeddings = chatbot._get_jina_embeddings_with_progress(texts)
    else:
        embeddings = chatbot.embedding_model.encode(texts, show_progress_bar=True)
    
    print(f"[DEBUG] Generated {len(embeddings)} embeddings, dimension: {len(embeddings[0]) if embeddings else 'N/A'}")
    
    # Add to Qdrant
    points_added = 0
    for chunk, embedding in zip(formatted_chunks, embeddings):
        point_id = chatbot.point_id_counter
        chatbot.metadata_store[point_id] = chunk['metadata']
        
        if hasattr(embedding, 'tolist'):
            vector = embedding.tolist()
        else:
            vector = embedding
        
        print(f"[DEBUG] Adding point {point_id} with vector dim: {len(vector)}")
        
        chatbot.qdrant_client.upsert(
            collection_name=chatbot.collection_name,
            points=[PointStruct(id=point_id, vector=vector, payload={
                'text': chunk['text'],
                'filename': chunk['metadata']['filename'],
                'page': chunk['metadata']['page'],
                'chunk_id': chunk['metadata']['chunk_id']
            })]
        )
        chatbot.point_id_counter += 1
        points_added += 1
    
    print(f"[DEBUG] Successfully added {points_added} points to collection '{chatbot.collection_name}'")
    print(f"[DEBUG] Total points in chatbot now: {chatbot.point_id_counter}")
    print(f"✅ Added {len(formatted_chunks)} chunks to the knowledge base")

@app.route('/api/embedding/import-json', methods=['POST'])
def import_json_to_embedding():
    """Import PPT JSON data into the embedding system"""
    try:
        print("=" * 60)
        print("DEBUG: Starting import_json_to_embedding")
        
        data = request.get_json()
        print(f"DEBUG: Got request data: {type(data)}")
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        json_data = data.get('json_data')
        session_id = session.get('session_id', 'default')
        
        print(f"DEBUG: Using session_id: {session_id}")
        print(f"DEBUG: json_data keys: {json_data.keys() if json_data else 'None'}")
        
        if not json_data:
            return jsonify({"error": "No json_data in request"}), 400
        
        if session_id not in chatbot_instances:
            print(f"DEBUG: Creating new chatbot instance for session: {session_id}")
            chatbot_instances[session_id] = {
                'chatbot': None,
                'documents': []
            }
        
        deck_name = json_data.get('deck', 'Unknown')
        model_used = json_data.get('model', 'Unknown')
        slides = json_data.get('slides', [])
        
        print(f"DEBUG: Deck: {deck_name}, Model: {model_used}, Slides: {len(slides)}")
        
        if not slides:
            return jsonify({"error": "No slides found in JSON data"}), 400
        
        chunks = []
        for slide in slides:
            slide_num = slide.get('number', 0)
            content = slide.get('content', '')
            
            if content and content.strip():
                chunk_text = f"[Slide {slide_num}]\n{content}"
                chunks.append(chunk_text)
        
        print(f"DEBUG: Created {len(chunks)} chunks")
        
        if not chunks:
            return jsonify({"error": "No text content extracted from slides"}), 400
        
        print(f"DEBUG: Checking if chatbot exists...")
        if not chatbot_instances[session_id]['chatbot']:
            print(f"DEBUG: Initializing AIDocumentChatbot with OpenAI key: {OPENAI_API_KEY[:10]}...")
            chatbot_instances[session_id]['chatbot'] = AIDocumentChatbot(
                openai_api_key=OPENAI_API_KEY,
                collection_name=f"docs_{session_id}"
            )
        
        print(f"DEBUG: Getting chatbot instance...")
        chatbot = chatbot_instances[session_id]['chatbot']
        
        print(f"DEBUG: Adding {len(chunks)} documents to chatbot...")
        add_text_chunks_to_chatbot(chatbot, chunks, deck_name)
        
        print(f"DEBUG: Documents added successfully!")
        
        chatbot_instances[session_id]['documents'].append({
            'filename': deck_name,
            'type': 'powerpoint',
            'slides': len(slides),
            'chunks': len(chunks),
            'model_used': model_used
        })
        
        print(f"DEBUG: Import completed successfully!")
        print("=" * 60)
        
        return jsonify({
            "success": True,
            "deck_name": deck_name,
            "slides_imported": len(slides),
            "chunks_created": len(chunks),
            "model_used": model_used
        })
    
    except Exception as e:
        print(f"DEBUG ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"DEBUG TRACEBACK:\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/ppt/get-models', methods=['GET'])
def get_ppt_models():
    """Get available models from PPT extraction service"""
    try:
        response = requests.get(f"{PPT_SERVICE_URL}/api/models", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Could not fetch models"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/embedding/debug', methods=['GET'])
def debug_embedding():
    """Debug endpoint to check session status"""
    session_id = session.get('session_id')
    
    if not session_id:
        return jsonify({"error": "No session", "session_id": None})
    
    if session_id not in chatbot_instances:
        return jsonify({
            "error": "Session not in instances",
            "session_id": session_id,
            "available_sessions": list(chatbot_instances.keys())
        })
    
    chatbot = chatbot_instances[session_id]['chatbot']
    
    return jsonify({
        "session_id": session_id,
        "point_count": chatbot.point_id_counter,
        "metadata_count": len(chatbot.metadata_store),
        "collection_name": chatbot.collection_name,
        "documents": chatbot_instances[session_id]['documents']
    })    


if __name__ == '__main__':
    print("=" * 60)
    print("AI Chatbot Server Starting")
    print("=" * 60)
    print(f"Ollama URL: {OLLAMA_BASE_URL}")
    print(f"OpenAI Available: {OPENAI_AVAILABLE}")
    print(f"Anthropic Available: {ANTHROPIC_AVAILABLE}")
    print(f"Embedding Available: {EMBEDDING_AVAILABLE}")
    print(f"PPT Service URL: {PPT_SERVICE_URL}")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)