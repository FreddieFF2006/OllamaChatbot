"""
Configuration file for AI Document Chatbot

Modify these settings to customize the chatbot's behavior.
"""

# ============================================================================
# API CONFIGURATION
# ============================================================================

# OpenAI API Configuration
OPENAI_MODEL = "gpt-4o-mini"  # Options: "gpt-4", "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.0      # Lower = more focused, Higher = more creative (0.0 - 1.0)
OPENAI_MAX_TOKENS = 1500      # Maximum tokens in response

# ============================================================================
# EMBEDDING CONFIGURATION
# ============================================================================

# Embedding Model
# Options:
# - 'sentence-transformers/all-MiniLM-L6-v2' (fast, 384 dimensions)
# - 'sentence-transformers/all-mpnet-base-v2' (better quality, 768 dimensions)
# - 'sentence-transformers/multi-qa-mpnet-base-dot-v1' (Q&A optimized)
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# ============================================================================
# RERANKING CONFIGURATION
# ============================================================================

# Reranker Model
# Options:
# - 'cross-encoder/ms-marco-MiniLM-L-6-v2' (fast, good quality)
# - 'cross-encoder/ms-marco-MiniLM-L-12-v2' (better quality, slower)
RERANKER_MODEL = 'cross-encoder/ms-marco-MiniLM-L-6-v2'

# ============================================================================
# SEARCH CONFIGURATION
# ============================================================================

# Vector Search Parameters
NUM_CANDIDATES = 1500      # Number of candidates to retrieve from vector search
NUM_RERANK = 625       # Number of results after reranking
VECTOR_DISTANCE = "COSINE"    # Distance metric: "COSINE", "EUCLIDEAN", or "DOT"

# ============================================================================
# DOCUMENT PROCESSING CONFIGURATION
# ============================================================================

# Text Chunking
CHUNK_SIZE = 500              # Target size for text chunks (characters)
CHUNK_OVERLAP = 200            # Overlap between chunks (characters)

# Supported File Extensions
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt']

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# Qdrant Configuration
QDRANT_COLLECTION_NAME = "documents"
QDRANT_IN_MEMORY = True       # Use in-memory database (False for persistent)
QDRANT_PATH = "./qdrant_db"   # Path for persistent storage (if IN_MEMORY=False)
QDRANT_HOST = "localhost"     # Host if using Qdrant server
QDRANT_PORT = 6333            # Port if using Qdrant server

# ============================================================================
# PROMPT CONFIGURATION
# ============================================================================

# System Prompt for OpenAI
SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on the provided document context. 
Always cite which source and page number you're referring to when answering. 
If the answer cannot be found in the provided context, say so clearly.
Be concise but thorough in your explanations."""

# User Prompt Template
USER_PROMPT_TEMPLATE = """Context from documents:
{context}

Question: {query}

Please provide a detailed answer based on the context above. Cite your sources with file names and page numbers."""

# ============================================================================
# DISPLAY CONFIGURATION
# ============================================================================

# Verbosity
VERBOSE = True                # Show pipeline steps during query
SHOW_SOURCES = True          # Display source information in results
SHOW_SCORES = True           # Display similarity/rerank scores

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================

# Batch Processing
EMBEDDING_BATCH_SIZE = 32    # Batch size for embedding generation
MAX_CONCURRENT_REQUESTS = 5   # Max concurrent API requests

# ============================================================================
# SAFETY & LIMITS
# ============================================================================

# Document Limits
MAX_FILE_SIZE_MB = 50        # Maximum file size in MB
MAX_DOCUMENTS = 1000         # Maximum number of documents to process at once
MAX_CHUNKS_PER_DOC = 10000  # Maximum chunks per document

# Query Limits
MAX_QUERY_LENGTH = 1000      # Maximum query length in characters
MIN_QUERY_LENGTH = 3         # Minimum query length in characters

# ============================================================================
# CACHE CONFIGURATION
# ============================================================================

# Caching (for future implementation)
ENABLE_CACHE = False         # Enable caching of embeddings
CACHE_DIR = "./cache"        # Directory for cache storage
CACHE_EXPIRY_DAYS = 30      # Cache expiry in days

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Logging
ENABLE_LOGGING = True        # Enable logging
LOG_LEVEL = "INFO"          # Log level: DEBUG, INFO, WARNING, ERROR
LOG_FILE = "chatbot.log"    # Log file name
LOG_TO_CONSOLE = True       # Also log to console

# ============================================================================
# ADVANCED CONFIGURATION
# ============================================================================

# Advanced Search Options
USE_HYBRID_SEARCH = False    # Combine vector and keyword search (future)
KEYWORD_WEIGHT = 0.3        # Weight for keyword search in hybrid mode

# Advanced Reranking
RERANK_THRESHOLD = 0.5      # Minimum rerank score to include in results

# Context Window Management
MAX_CONTEXT_TOKENS = 8000   # Maximum tokens to send to OpenAI
CONTEXT_BUFFER = 500        # Buffer tokens for response
