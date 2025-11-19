# 🤖 AI Chatbot with Ollama & PowerPoint Extraction

A comprehensive AI chatbot system featuring document embedding, RAG, and PowerPoint extraction using vision models.

## Features

- Multi-provider AI support (Ollama, OpenAI, Anthropic)
- Document Q&A with vector search & reranking
- PowerPoint extraction using GPT-4o/Claude/Gemini
- Real-time streaming chat interface

## Quick Start

1. Clone the repository
```bash
git clone https://github.com/FreddieFF2006/OllamaChatbot.git
cd OllamaChatbot
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your API keys
```bash
copy .env.example .env
# Edit .env with your actual keys
```

4. Run the application
```bash
python app.py
```

5. Open http://localhost:5000

## Environment Variables

Required API keys (add to `.env`):
- `OPENAI_API_KEY` - For GPT models
- `COHERE_API_KEY` - For reranking
- `JINA_API_KEY` - For embeddings

## Tech Stack

- Flask, Python
- Ollama, OpenAI, Anthropic
- Qdrant vector database
- Cohere reranking
- Vision AI for PPT extraction

## License

MIT