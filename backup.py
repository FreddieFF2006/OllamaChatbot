"""
EMBEDDING
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Embedding - AI Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --navy-blue: #1e3a5f;
            --dark-navy: #152a45;
            --light-navy: #2d5a8c;
            --accent-blue: #4a9eff;
            --bg-gray: #f7f9fc;
            --border-gray: #e5e7eb;
            --text-dark: #1f2937;
            --text-light: #6b7280;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--bg-gray);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            color: var(--text-dark);
        }

        .header {
            background: white;
            padding: 1rem 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-gray);
        }

        .header h1 {
            font-size: 1.5rem;
            color: var(--navy-blue);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
        }

        .back-button {
            background: var(--navy-blue);
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.95rem;
            text-decoration: none;
            transition: background 0.2s;
            font-weight: 500;
        }

        .back-button:hover {
            background: var(--dark-navy);
        }

        .container {
            flex: 1;
            max-width: 1400px;
            width: 100%;
            margin: 2rem auto;
            padding: 0 2rem;
            display: flex;
            gap: 2rem;
        }

        .upload-section {
            flex: 0 0 350px;
            background: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            height: fit-content;
            border: 1px solid var(--border-gray);
        }

        .chat-section {
            flex: 1;
            background: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            max-height: calc(100vh - 200px);
            border: 1px solid var(--border-gray);
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: var(--navy-blue);
        }

        .upload-area {
            border: 2px dashed var(--accent-blue);
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 1rem;
            background: #fafbfc;
        }

        .upload-area:hover {
            background: #f0f7ff;
            border-color: var(--navy-blue);
        }

        .upload-area.dragover {
            background: #f0f3ff;
            border-color: #5568d3;
        }

        #fileInput {
            display: none;
        }

        .upload-icon {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }

        .file-list {
            margin-top: 1rem;
            max-height: 200px;
            overflow-y: auto;
        }

        .file-item {
            background: var(--bg-gray);
            padding: 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid var(--border-gray);
        }

        .btn {
            width: 100%;
            padding: 0.75rem;
            border: none;
            border-radius: 6px;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }

        .btn-primary {
            background: var(--navy-blue);
            color: white;
            margin-bottom: 0.5rem;
        }

        .btn-primary:hover {
            background: var(--dark-navy);
        }

        .btn-primary:disabled {
            background: #d1d5db;
            cursor: not-allowed;
        }

        .btn-secondary {
            background: var(--bg-gray);
            color: var(--navy-blue);
            border: 1px solid var(--border-gray);
        }

        .btn-secondary:hover {
            background: #e5e7eb;
        }

        .status {
            padding: 0.75rem;
            border-radius: 6px;
            margin-top: 1rem;
            font-size: 0.9rem;
        }

        .status.success {
            background: #d4edda;
            color: #155724;
        }

        .status.error {
            background: #f8d7da;
            color: #721c24;
        }

        .status.info {
            background: #d1ecf1;
            color: #0c5460;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 1rem;
            padding: 1rem;
            background: var(--bg-gray);
            border-radius: 8px;
        }

        .message {
            margin-bottom: 1.5rem;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message-label {
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-light);
        }

        .message-content {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid var(--border-gray);
            line-height: 1.8;
        }

        .message-content h1,
        .message-content h2,
        .message-content h3,
        .message-content h4 {
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            font-weight: 600;
            color: var(--navy-blue);
        }

        .message-content h1 { font-size: 1.5rem; }
        .message-content h2 { font-size: 1.3rem; }
        .message-content h3 { font-size: 1.15rem; }
        .message-content h4 { font-size: 1rem; }

        .message-content h1:first-child,
        .message-content h2:first-child,
        .message-content h3:first-child {
            margin-top: 0;
        }

        .message-content ul,
        .message-content ol {
            margin: 1rem 0;
            padding-left: 1.5rem;
        }

        .message-content li {
            margin: 0.5rem 0;
            line-height: 1.6;
        }

        .message-content strong {
            font-weight: 600;
            color: var(--text-dark);
        }

        .message-content p {
            margin: 0.75rem 0;
        }

        .message-content code {
            background: var(--bg-gray);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: var(--navy-blue);
        }

        .message-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        .message-content table th,
        .message-content table td {
            border: 1px solid var(--border-gray);
            padding: 0.5rem;
            text-align: left;
        }

        .message-content table th {
            background: var(--bg-gray);
            font-weight: 600;
            color: var(--navy-blue);
        }

        .message-content blockquote {
            border-left: 4px solid var(--accent-blue);
            padding-left: 1rem;
            margin: 1rem 0;
            color: var(--text-light);
            font-style: italic;
        }

        .message-content hr {
            border: none;
            border-top: 2px solid var(--border-gray);
            margin: 1.5rem 0;
        }

        .message.user .message-content {
            background: var(--navy-blue);
            color: white;
            border-color: var(--navy-blue);
        }

        .sources-section {
            margin-top: 1rem;
            background: var(--bg-gray);
            border-radius: 6px;
            font-size: 0.9rem;
            overflow: hidden;
            border: 1px solid var(--border-gray);
        }

        .sources-header {
            padding: 0.75rem 1rem;
            background: var(--navy-blue);
            color: white;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
            transition: background 0.2s;
        }

        .sources-header:hover {
            background: var(--dark-navy);
        }

        .sources-header strong {
            font-weight: 600;
        }

        .toggle-icon {
            font-size: 1.2rem;
            transition: transform 0.3s;
        }

        .toggle-icon.collapsed {
            transform: rotate(-90deg);
        }

        .sources-content {
            max-height: 500px;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            padding: 1rem;
            background: white;
        }

        .sources-content.collapsed {
            max-height: 0;
            padding: 0 1rem;
        }

        .source-item {
            padding: 0.75rem;
            margin: 0.5rem 0;
            background: var(--bg-gray);
            border-radius: 6px;
            border-left: 3px solid var(--accent-blue);
            border: 1px solid var(--border-gray);
            border-left: 3px solid var(--accent-blue);
        }

        .input-area {
            display: flex;
            gap: 0.5rem;
        }

        .input-area input {
            flex: 1;
            padding: 0.75rem 1rem;
            border: 1px solid var(--border-gray);
            border-radius: 6px;
            font-size: 0.95rem;
            transition: all 0.2s;
            background: white;
        }

        .input-area input:focus {
            outline: none;
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
        }

        .input-area button {
            padding: 0.75rem 1.5rem;
            background: var(--navy-blue);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 500;
            transition: background 0.2s;
        }

        .input-area button:hover:not(:disabled) {
            background: var(--dark-navy);
        }

        .input-area button:disabled {
            background: #d1d5db;
            cursor: not-allowed;
        }

        .loading {
            display: inline-block;
            width: 1rem;
            height: 1rem;
            border: 2px solid var(--border-gray);
            border-top: 2px solid var(--navy-blue);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .welcome-message {
            text-align: center;
            padding: 3rem 2rem;
            color: var(--text-light);
        }

        .welcome-message h2 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--navy-blue);
        }

        .config-info {
            background: var(--bg-gray);
            padding: 1rem;
            border-radius: 6px;
            margin-top: 1rem;
            font-size: 0.85rem;
            color: var(--text-light);
            border: 1px solid var(--border-gray);
        }

        .config-info strong {
            color: var(--navy-blue);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>
            📚 Document Embedding & Q&A
        </h1>
        <a href="/" class="back-button">← Back to Chat</a>
    </div>

    <div class="container">
        <!-- Upload Section -->
        <div class="upload-section">
            <h2 class="section-title">Upload Documents</h2>
            
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📄</div>
                <p><strong>Click to upload</strong> or drag and drop</p>
                <p style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">
                    PDF, DOCX, TXT files
                </p>
            </div>
            
            <input type="file" id="fileInput" multiple accept=".pdf,.docx,.doc,.txt">
            
            <div class="file-list" id="fileList"></div>
            
            <button class="btn btn-primary" id="initBtn">Initialize Chatbot</button>
            <button class="btn btn-primary" id="uploadBtn" disabled>Process Documents</button>
            <button class="btn btn-secondary" id="resetBtn">Reset Session</button>
            
            <div id="status"></div>

            <div class="config-info">
                <strong>Configuration:</strong><br>
                Candidates: <span id="configCandidates">1500</span><br>
                Rerank: <span id="configRerank">625</span><br>
                Model: GPT-4o-mini
            </div>
        </div>

        <!-- Chat Section -->
        <div class="chat-section">
            <h2 class="section-title">Ask Questions</h2>
            
            <div class="chat-messages" id="chatMessages">
                <div class="welcome-message">
                    <h2>Welcome to Document Q&A</h2>
                    <p>Initialize the chatbot and upload documents to get started.</p>
                    <p style="margin-top: 1rem; font-size: 0.9rem;">
                        The system uses vector search with reranking to find<br>
                        the most relevant information from your documents.
                    </p>
                </div>
            </div>
            
            <div class="input-area">
                <input 
                    type="text" 
                    id="questionInput" 
                    placeholder="Ask a question about your documents..." 
                    disabled
                >
                <button id="askBtn" disabled>Ask</button>
            </div>
        </div>
    </div>

    <script>
        let selectedFiles = [];
        let isInitialized = false;
        let documentsLoaded = false;

        // DOM Elements
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileList = document.getElementById('fileList');
        const initBtn = document.getElementById('initBtn');
        const uploadBtn = document.getElementById('uploadBtn');
        const resetBtn = document.getElementById('resetBtn');
        const status = document.getElementById('status');
        const chatMessages = document.getElementById('chatMessages');
        const questionInput = document.getElementById('questionInput');
        const askBtn = document.getElementById('askBtn');

        // Upload area click
        uploadArea.addEventListener('click', () => fileInput.click());

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });

        // File input change
        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });

        function handleFiles(files) {
            selectedFiles = Array.from(files);
            displayFiles();
            if (selectedFiles.length > 0 && isInitialized) {
                uploadBtn.disabled = false;
            }
        }

        function displayFiles() {
            fileList.innerHTML = '';
            selectedFiles.forEach((file, index) => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.innerHTML = `
                    <span>📄 ${file.name}</span>
                    <button onclick="removeFile(${index})" style="background: none; border: none; cursor: pointer; color: #dc3545; font-weight: bold;">×</button>
                `;
                fileList.appendChild(fileItem);
            });
        }

        function removeFile(index) {
            selectedFiles.splice(index, 1);
            displayFiles();
            if (selectedFiles.length === 0) {
                uploadBtn.disabled = true;
            }
        }

        function showStatus(message, type = 'info') {
            status.innerHTML = `<div class="status ${type}">${message}</div>`;
        }

        // Initialize chatbot
        initBtn.addEventListener('click', async () => {
            initBtn.disabled = true;
            initBtn.innerHTML = '<span class="loading"></span> Initializing...';
            
            try {
                const response = await fetch('/api/embedding/init', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });

                const data = await response.json();

                if (data.success) {
                    isInitialized = true;
                    showStatus('✅ Chatbot initialized! Upload documents to begin.', 'success');
                    initBtn.innerHTML = '✓ Initialized';
                    if (selectedFiles.length > 0) {
                        uploadBtn.disabled = false;
                    }
                } else {
                    throw new Error(data.error || 'Initialization failed');
                }
            } catch (error) {
                showStatus('❌ Error: ' + error.message, 'error');
                initBtn.disabled = false;
                initBtn.innerHTML = 'Initialize Chatbot';
            }
        });

        // Upload documents
        uploadBtn.addEventListener('click', async () => {
            if (selectedFiles.length === 0) {
                showStatus('❌ Please select files first', 'error');
                return;
            }

            uploadBtn.disabled = true;
            uploadBtn.innerHTML = '<span class="loading"></span> Processing...';

            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('files', file);
            });

            try {
                const response = await fetch('/api/embedding/upload', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    documentsLoaded = true;
                    showStatus(`✅ ${data.message}`, 'success');
                    uploadBtn.innerHTML = '✓ Documents Processed';
                    questionInput.disabled = false;
                    askBtn.disabled = false;
                    
                    // Clear welcome message
                    chatMessages.innerHTML = '';
                    addMessage('system', `Documents loaded: ${data.files.join(', ')}`);
                } else {
                    throw new Error(data.error || 'Upload failed');
                }
            } catch (error) {
                showStatus('❌ Error: ' + error.message, 'error');
                uploadBtn.disabled = false;
                uploadBtn.innerHTML = 'Process Documents';
            }
        });

        // Reset session
        resetBtn.addEventListener('click', async () => {
            if (confirm('Are you sure you want to reset? This will clear all documents.')) {
                try {
                    await fetch('/api/embedding/reset', { method: 'POST' });
                    location.reload();
                } catch (error) {
                    showStatus('❌ Error resetting session', 'error');
                }
            }
        });

        // Ask question
        async function askQuestion() {
            const question = questionInput.value.trim();
            if (!question) return;

            addMessage('user', question);
            questionInput.value = '';
            questionInput.disabled = true;
            askBtn.disabled = true;
            askBtn.innerHTML = '<span class="loading"></span>';

            try {
                const response = await fetch('/api/embedding/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });

                const data = await response.json();

                if (data.success) {
                    addMessage('assistant', data.answer, data.sources);
                } else {
                    throw new Error(data.error || 'Query failed');
                }
            } catch (error) {
                addMessage('system', '❌ Error: ' + error.message);
            } finally {
                questionInput.disabled = false;
                askBtn.disabled = false;
                askBtn.innerHTML = 'Ask';
                questionInput.focus();
            }
        }

        askBtn.addEventListener('click', askQuestion);
        questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !askBtn.disabled) {
                askQuestion();
            }
        });

        // Simple markdown parser
        function parseMarkdown(text) {
            // Escape HTML first
            text = text.replace(/&/g, '&amp;')
                       .replace(/</g, '&lt;')
                       .replace(/>/g, '&gt;');

            // Headers
            text = text.replace(/^### (.*$)/gm, '<h3>$1</h3>');
            text = text.replace(/^## (.*$)/gm, '<h2>$1</h2>');
            text = text.replace(/^# (.*$)/gm, '<h1>$1</h1>');

            // Bold
            text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
            text = text.replace(/__(.+?)__/g, '<strong>$1</strong>');

            // Italic
            text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
            text = text.replace(/_(.+?)_/g, '<em>$1</em>');

            // Lists - handle numbered and bullet points
            text = text.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
            text = text.replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>');
            
            // Wrap consecutive <li> in <ol> or <ul>
            text = text.replace(/(<li>.*<\/li>\n?)+/g, function(match) {
                if (match.includes('1.')) {
                    return '<ol>' + match + '</ol>';
                } else {
                    return '<ul>' + match + '</ul>';
                }
            });

            // Line breaks - convert double newlines to paragraphs
            text = text.split('\n\n').map(para => {
                if (para.trim() && !para.startsWith('<h') && !para.startsWith('<ul') && !para.startsWith('<ol')) {
                    return '<p>' + para.replace(/\n/g, '<br>') + '</p>';
                }
                return para;
            }).join('\n');

            // Code blocks
            text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

            return text;
        }

        function addMessage(type, content, sources = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            let label = type === 'user' ? '👤 You' : type === 'assistant' ? '🤖 AI Assistant' : 'ℹ️ System';
            
            // Parse markdown for assistant messages
            const formattedContent = type === 'assistant' ? parseMarkdown(content) : content;
            
            messageDiv.innerHTML = `
                <div class="message-label">${label}</div>
                <div class="message-content">${formattedContent}</div>
            `;

            if (sources && sources.length > 0) {
                const sourcesId = 'sources-' + Date.now();
                const sourcesHtml = `
                    <div class="sources-section">
                        <div class="sources-header" onclick="toggleSources('${sourcesId}')">
                            <strong>📚 Sources (${sources.length})</strong>
                            <span class="toggle-icon" id="${sourcesId}-icon">▼</span>
                        </div>
                        <div class="sources-content" id="${sourcesId}">
                            ${sources.map((s, i) => `
                                <div class="source-item">
                                    <strong>${i + 1}. ${s.filename}</strong> - Page ${s.page}
                                    <br><small>Chunk ${s.chunk_id} | Score: ${typeof s.score === 'number' ? s.score.toFixed(4) : s.score}</small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
                messageDiv.innerHTML += sourcesHtml;
            }

            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Toggle sources visibility
        function toggleSources(sourcesId) {
            const content = document.getElementById(sourcesId);
            const icon = document.getElementById(sourcesId + '-icon');
            
            if (content && icon) {
                content.classList.toggle('collapsed');
                icon.classList.toggle('collapsed');
            }
        }

        // Check embedding availability on load
        fetch('/api/embedding/status')
            .then(r => r.json())
            .then(data => {
                if (!data.available) {
                    showStatus('❌ Embedding feature not available. Install dependencies.', 'error');
                    initBtn.disabled = true;
                } else if (!data.openai_configured) {
                    showStatus('❌ OpenAI API key not configured', 'error');
                    initBtn.disabled = true;
                }
            });
    </script>
</body>
</html>
"""

"""
APP
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

# ============================================================================
# EMBEDDING ROUTES
# ============================================================================

@app.route('/api/embedding/status', methods=['GET'])
def embedding_status():
    """Check if embedding feature is available"""
    return jsonify({
        "available": EMBEDDING_AVAILABLE,
        "openai_configured": bool(OPENAI_API_KEY)
    })

@app.route('/api/embedding/init', methods=['POST'])
def init_embedding():
    """Initialize a new chatbot instance for the session"""
    if not EMBEDDING_AVAILABLE:
        return jsonify({"error": "Embedding feature not available"}), 503
    
    if not OPENAI_API_KEY:
        return jsonify({"error": "OpenAI API key not configured"}), 400
    
    try:
        # Create a unique session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = secrets.token_hex(16)
        
        session_id = session['session_id']
        
        # Initialize chatbot for this session
        chatbot = AIDocumentChatbot(
            openai_api_key=OPENAI_API_KEY,
            collection_name=f"documents_{session_id}"
        )
        
        chatbot_instances[session_id] = chatbot
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Chatbot initialized successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/embedding/upload', methods=['POST'])
def upload_documents():
    """Handle document upload and processing"""
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
        chatbot = chatbot_instances[session_id]
        
        # Save uploaded files temporarily
        upload_folder = f"/tmp/uploads_{session_id}"
        os.makedirs(upload_folder, exist_ok=True)
        
        file_paths = []
        for file in files:
            if file.filename:
                file_path = os.path.join(upload_folder, file.filename)
                file.save(file_path)
                file_paths.append(file_path)
        
        # Process documents
        chatbot.add_documents(file_paths)
        
        return jsonify({
            "success": True,
            "message": f"Successfully processed {len(file_paths)} document(s)",
            "files": [os.path.basename(fp) for fp in file_paths]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/embedding/query', methods=['POST'])
def query_documents():
    """Query the embedded documents"""
    if not EMBEDDING_AVAILABLE:
        return jsonify({"error": "Embedding feature not available"}), 503
    
    session_id = session.get('session_id')
    if not session_id or session_id not in chatbot_instances:
        return jsonify({"error": "Chatbot not initialized or no documents loaded"}), 400
    
    data = request.json
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        chatbot = chatbot_instances[session_id]
        
        # Import config if needed
        import config
        
        # Query the chatbot
        result = chatbot.query(
            question,
            num_candidates=config.NUM_CANDIDATES,
            num_rerank=config.NUM_RERANK,
            verbose=False
        )
        
        # Format sources
        sources = []
        for source in result['sources']:
            sources.append({
                'filename': source['metadata']['filename'],
                'page': source['metadata']['page'],
                'chunk_id': source['metadata']['chunk_id'],
                'score': source.get('rerank_score', 'N/A'),
                'text': source['text'][:200] + "..."  # Preview
            })
        
        return jsonify({
            "success": True,
            "answer": result['answer'],
            "sources": sources,
            "num_candidates": result['num_candidates'],
            "num_reranked": result['num_reranked']
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/embedding/reset', methods=['POST'])
def reset_embedding():
    """Reset the embedding session"""
    session_id = session.get('session_id')
    if session_id and session_id in chatbot_instances:
        del chatbot_instances[session_id]
        
        # Clean up temporary files
        upload_folder = f"/tmp/uploads_{session_id}"
        if os.path.exists(upload_folder):
            import shutil
            shutil.rmtree(upload_folder)
    
    session.pop('session_id', None)
    
    return jsonify({"success": True, "message": "Session reset successfully"})

if __name__ == '__main__':
    print("Starting AI Chatbot Server...")
    print("Make sure Ollama is running on http://localhost:11434")
    print("Access the chatbot at http://localhost:5000")
    print("Access document embedding at http://localhost:5000/embedding")
    app.run(debug=True, host='0.0.0.0', port=5000)

    



    AI CHATBOT
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
        
        # Initialize embedding model (AllMiniLM)
        print("Loading JinaAI embedding model...")
        import requests
        self.jina_api_key = os.getenv("JINA_API_KEY")
        self.use_jina = True if self.jina_api_key else False

        if self.use_jina:
            self.embedding_dim = 768
            print("Using JinaAI embeddings")
        else:
            #Fallback to local model
            self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
            self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
            print(f"Using {config.EMBEDDING_MODEL}")
        
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

    
    def get_answer_from_openai(self, query: str, context_chunks: List[Dict]) -> str:
        """
        Step 5: Pass the top pages/chunks to OpenAI API to generate an answer.
        
        Args:
            query: User's question
            context_chunks: Top relevant chunks after reranking
            
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
        
        # Call OpenAI API
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content # type: ignore
    
    def query(self, question: str, num_candidates: int = None, num_rerank: int = None, verbose: bool = True): # type: ignore
        if num_candidates is None:
            num_candidates = config.NUM_CANDIDATES
        if num_rerank is None:
            num_rerank = config.NUM_RERANK

        
        """
        Complete query pipeline: search, rerank, and get AI answer.
        
        Args:
            question: User's question
            num_candidates: Number of candidates to retrieve from vector search
            num_rerank: Number of top results after reranking
            verbose: Whether to print intermediate steps
            
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
        
        # Step 5: Get answer from OpenAI
        if verbose:
            print(f"Step 5: Generating answer with OpenAI...\n")
        answer = self.get_answer_from_openai(question, reranked_results)
        
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