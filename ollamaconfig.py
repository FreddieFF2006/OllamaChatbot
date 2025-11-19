# Configuration file for AI Chatbot

# Ollama API Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TIMEOUT = 60  # seconds

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Default Model Settings
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MODEL = "llama2"

# Chat Settings
MAX_HISTORY_LENGTH = 50  # Maximum number of messages to keep in history
STREAM_ENABLED = True

# UI Settings
APP_TITLE = "AI Chatbot"
ENABLE_MARKDOWN = True

# Advanced Settings
REQUEST_TIMEOUT = 60  # HTTP request timeout in seconds
RETRY_ATTEMPTS = 3
