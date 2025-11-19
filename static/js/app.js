// AI Chatbot Application
class ChatBot {
    constructor() {
        this.messages = [];
        this.currentModel = '';
        this.currentProvider = 'ollama';
        this.isStreaming = false;
        
        this.initElements();
        this.initEventListeners();
        this.checkHealth();
        this.loadModels();
    }

    initElements() {
        // UI Elements
        this.chatContainer = document.getElementById('chatContainer');
        this.messageInput = document.getElementById('messageInput');
        this.chatForm = document.getElementById('chatForm');
        this.sendBtn = document.getElementById('sendBtn');
        this.modelSelect = document.getElementById('modelSelect');
        this.refreshModelsBtn = document.getElementById('refreshModels');
        this.clearChatBtn = document.getElementById('clearChat');
        this.temperatureSlider = document.getElementById('temperature');
        this.tempValue = document.getElementById('tempValue');
        this.chatMode = document.getElementById('chatMode');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
    }

    initEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });

        // Enter to send (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Model selection
        this.modelSelect.addEventListener('change', (e) => {
            const selectedOption = e.target.selectedOptions[0];
            this.currentModel = e.target.value;
            this.currentProvider = selectedOption.dataset.provider || 'ollama';
            console.log('Model changed to:', this.currentModel, 'Provider:', this.currentProvider);
        });

        // Refresh models
        this.refreshModelsBtn.addEventListener('click', () => {
            this.loadModels();
        });

        // Clear chat
        this.clearChatBtn.addEventListener('click', () => {
            this.clearChat();
        });

        // Temperature slider
        this.temperatureSlider.addEventListener('input', (e) => {
            this.tempValue.textContent = e.target.value;
        });
    }

    async checkHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (data.ollama_connected) {
                this.updateStatus('connected', 'Connected');
            } else {
                this.updateStatus('disconnected', 'Ollama Offline');
            }
        } catch (error) {
            this.updateStatus('disconnected', 'Server Offline');
            console.error('Health check failed:', error);
        }
    }

    updateStatus(status, text) {
        this.statusDot.className = `status-dot ${status}`;
        this.statusText.textContent = text;
    }

    async loadModels() {
        try {
            this.updateStatus('connecting', 'Loading models...');
            
            const response = await fetch('/api/models');
            const data = await response.json();

            if (data.success && data.models.length > 0) {
                this.modelSelect.innerHTML = '';
                
                // Group models by provider
                const ollamaModels = data.models.filter(m => m.provider === 'ollama');
                const openaiModels = data.models.filter(m => m.provider === 'openai');
                const anthropicModels = data.models.filter(m => m.provider === 'anthropic');
                
                // Add Ollama models
                if (ollamaModels.length > 0) {
                    const ollamaGroup = document.createElement('optgroup');
                    ollamaGroup.label = '🏠 Local Ollama Models';
                    ollamaModels.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model.name;
                        option.textContent = model.name;
                        option.dataset.provider = 'ollama';
                        ollamaGroup.appendChild(option);
                    });
                    this.modelSelect.appendChild(ollamaGroup);
                }
                
                // Add OpenAI models
                if (openaiModels.length > 0) {
                    const openaiGroup = document.createElement('optgroup');
                    openaiGroup.label = '🤖 OpenAI Models (ChatGPT)';
                    openaiModels.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model.name;
                        option.textContent = model.name;
                        option.dataset.provider = 'openai';
                        openaiGroup.appendChild(option);
                    });
                    this.modelSelect.appendChild(openaiGroup);
                }
                
                // Add Anthropic Claude models
                if (anthropicModels.length > 0) {
                    const anthropicGroup = document.createElement('optgroup');
                    anthropicGroup.label = '🧠 Anthropic Models (Claude)';
                    anthropicModels.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model.name;
                        // Display user-friendly names
                        let displayName = model.name;
                        if (model.name.includes('sonnet')) {
                            displayName = model.name.replace('claude-3-5-sonnet', 'Claude 3.5 Sonnet')
                                                   .replace('claude-3-sonnet', 'Claude 3 Sonnet');
                        } else if (model.name.includes('opus')) {
                            displayName = model.name.replace('claude-3-opus', 'Claude 3 Opus');
                        } else if (model.name.includes('haiku')) {
                            displayName = model.name.replace('claude-3-5-haiku', 'Claude 3.5 Haiku')
                                                   .replace('claude-3-haiku', 'Claude 3 Haiku');
                        }
                        option.textContent = displayName;
                        option.dataset.provider = 'anthropic';
                        anthropicGroup.appendChild(option);
                    });
                    this.modelSelect.appendChild(anthropicGroup);
                }

                // Set first model as default
                const firstOption = this.modelSelect.options[0];
                this.currentModel = firstOption.value;
                this.currentProvider = firstOption.dataset.provider || 'ollama';
                
                this.updateStatus('connected', 'Connected');
                console.log('Models loaded:', data.models.length);
                
                if (data.openai_available) {
                    console.log('OpenAI models available');
                }
                if (data.anthropic_available) {
                    console.log('Anthropic Claude models available');
                }
            } else {
                this.modelSelect.innerHTML = '<option value="">No models found</option>';
                this.updateStatus('disconnected', 'No models available');
                
                if (data.error) {
                    this.showError(`Failed to load models: ${data.error}`);
                }
            }
        } catch (error) {
            this.modelSelect.innerHTML = '<option value="">Error loading models</option>';
            this.updateStatus('disconnected', 'Connection Error');
            console.error('Failed to load models:', error);
            this.showError('Failed to connect to server');
        }
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isStreaming) {
            return;
        }

        if (!this.currentModel) {
            this.showError('Please select a model first');
            return;
        }

        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';

        // Remove welcome message if present
        const welcomeMsg = this.chatContainer.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }

        // Add user message
        this.addMessage('user', message);
        this.messages.push({ role: 'user', content: message });

        // Show typing indicator
        const typingId = this.showTypingIndicator();

        // Disable send button
        this.isStreaming = true;
        this.sendBtn.disabled = true;

        try {
            const mode = this.chatMode.value;
            const temperature = parseFloat(this.temperatureSlider.value);

            if (mode === 'chat') {
                await this.streamChatResponse(this.messages, temperature, typingId);
            } else {
                await this.streamGenerateResponse(message, temperature, typingId);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.removeTypingIndicator(typingId);
            this.showError('Failed to get response from AI');
        } finally {
            this.isStreaming = false;
            this.sendBtn.disabled = false;
            this.messageInput.focus();
        }
    }

    async streamChatResponse(messages, temperature, typingId) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: this.currentModel,
                messages: messages,
                temperature: temperature,
                provider: this.currentProvider
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        this.removeTypingIndicator(typingId);
        const messageId = this.addMessage('assistant', '');
        
        await this.processStream(response, messageId);
    }

    async streamGenerateResponse(prompt, temperature, typingId) {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: this.currentModel,
                prompt: prompt,
                temperature: temperature,
                provider: this.currentProvider
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        this.removeTypingIndicator(typingId);
        const messageId = this.addMessage('assistant', '');
        
        await this.processStream(response, messageId);
    }

    async processStream(response, messageId) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';

        while (true) {
            const { done, value } = await reader.read();
            
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        
                        if (data.error) {
                            this.showError(data.error);
                            break;
                        }
                        
                        if (data.content) {
                            fullContent += data.content;
                            this.updateMessage(messageId, fullContent);
                        }
                        
                        if (data.done) {
                            this.messages.push({
                                role: 'assistant',
                                content: fullContent
                            });
                        }
                    } catch (e) {
                        console.error('Error parsing SSE data:', e);
                    }
                }
            }
        }
    }

    addMessage(role, content) {
        const messageId = `msg-${Date.now()}-${Math.random()}`;
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        messageDiv.id = messageId;

        const avatar = role === 'user' ? 'U' : 'AI';
        const sender = role === 'user' ? 'You' : 'Assistant';

        messageDiv.innerHTML = `
            <div class="message-header">
                <div class="message-avatar ${role}-avatar">${avatar}</div>
                <span class="message-sender">${sender}</span>
            </div>
            <div class="message-content">${this.formatContent(content)}</div>
        `;

        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();

        return messageId;
    }

    updateMessage(messageId, content) {
        const messageDiv = document.getElementById(messageId);
        if (messageDiv) {
            const contentDiv = messageDiv.querySelector('.message-content');
            contentDiv.innerHTML = this.formatContent(content);
            this.scrollToBottom();
        }
    }

    formatContent(content) {
        if (!content) return '';
        
        // Convert markdown-style code blocks
        content = content.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
        
        // Convert inline code
        content = content.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Convert line breaks
        content = content.replace(/\n/g, '<br>');
        
        return content;
    }

    showTypingIndicator() {
        const typingId = `typing-${Date.now()}`;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant-message';
        typingDiv.id = typingId;

        typingDiv.innerHTML = `
            <div class="message-header">
                <div class="message-avatar assistant-avatar">AI</div>
                <span class="message-sender">Assistant</span>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;

        this.chatContainer.appendChild(typingDiv);
        this.scrollToBottom();

        return typingId;
    }

    removeTypingIndicator(typingId) {
        const typingDiv = document.getElementById(typingId);
        if (typingDiv) {
            typingDiv.remove();
        }
    }

    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            this.messages = [];
            this.chatContainer.innerHTML = `
                <div class="welcome-message">
                    <h2>Welcome to AI Chatbot</h2>
                    <p>Select a model and start chatting!</p>
                    <div class="features">
                        <div class="feature-item">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <circle cx="12" cy="12" r="10"></circle>
                                <path d="M12 16v-4M12 8h.01"></path>
                            </svg>
                            <span>Supports local Ollama models</span>
                        </div>
                        <div class="feature-item">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                <circle cx="9" cy="7" r="4"></circle>
                                <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"></path>
                            </svg>
                            <span>Cloud model integration</span>
                        </div>
                        <div class="feature-item">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
                            </svg>
                            <span>Real-time streaming responses</span>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message assistant-message';
        errorDiv.innerHTML = `
            <div class="message-header">
                <div class="message-avatar assistant-avatar">⚠️</div>
                <span class="message-sender">System</span>
            </div>
            <div class="message-content" style="color: var(--danger-color);">
                ${message}
            </div>
        `;
        this.chatContainer.appendChild(errorDiv);
        this.scrollToBottom();
    }

    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }
}

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatBot();
});