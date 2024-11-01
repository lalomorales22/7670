# app.py
from flask import Flask, render_template_string, request, jsonify
import requests
import sqlite3
import os
from datetime import datetime, timezone
from functools import wraps
from contextlib import contextmanager
import logging
import time
from typing import Optional, Dict, Any
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    GROK_API_KEY = os.environ.get('XAI_API_KEY')
    GROK_API_URL = 'https://api.x.ai/v1/chat/completions'
    DATABASE_PATH = 'chat_history.db'
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    RATE_LIMIT_REQUESTS = 60
    RATE_LIMIT_WINDOW = 60  # seconds
    MAX_MESSAGE_LENGTH = 4000
    MIN_MESSAGE_LENGTH = 1

# Redis connection for rate limiting
redis_client = redis.from_url(Config.REDIS_URL)

# Database management
@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()

def init_db():
    """Initialize database with proper schema"""
    schema = '''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'sent',
        retry_count INTEGER DEFAULT 0,
        error_message TEXT
    );
    '''
    try:
        with get_db_connection() as conn:
            conn.executescript(schema)
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

# Initialize database on startup
init_db()

# Rate limiting decorator
def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        pipe = redis_client.pipeline()
        now = time.time()
        key = f'rate_limit:{request.remote_addr}'

        pipe.zremrangebyscore(key, 0, now - Config.RATE_LIMIT_WINDOW)
        pipe.zadd(key, {now: now})
        pipe.zcard(key)
        pipe.expire(key, Config.RATE_LIMIT_WINDOW)
        results = pipe.execute()

        request_count = results[2]

        if request_count > Config.RATE_LIMIT_REQUESTS:
            return jsonify({'error': 'Rate limit exceeded'}), 429

        return f(*args, **kwargs)
    return decorated_function

# Input validation
def validate_message(message: str) -> str:
    """Validate and sanitize user input"""
    if not isinstance(message, str):
        raise ValueError("Message must be a string")

    message = message.strip()

    if len(message) < Config.MIN_MESSAGE_LENGTH:
        raise ValueError("Message is too short")

    if len(message) > Config.MAX_MESSAGE_LENGTH:
        raise ValueError(f"Message exceeds maximum length of {Config.MAX_MESSAGE_LENGTH} characters")

    return message

# API interaction
def make_grok_request(message: str) -> str:
    """Make a request to the Grok API with error handling"""
    if not Config.GROK_API_KEY:
        raise ValueError("API key is not configured")

    headers = {
        'Authorization': f'Bearer {Config.GROK_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'grok-beta',
        'messages': [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        'temperature': 0.7,
        'max_tokens': 1000
    }

    try:
        response = requests.post(
            Config.GROK_API_URL,
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()

        result = response.json()
        if 'choices' not in result or not result['choices']:
            raise ValueError("Invalid API response structure")

        return result['choices'][0]['message']['content']

    except requests.Timeout:
        raise ValueError("Request to Grok API timed out")
    except requests.RequestException as e:
        logger.error(f"Grok API request failed: {str(e)}")
        raise ValueError(f"Failed to get response from Grok API: {str(e)}")

# Database operations
def store_message(role: str, content: str, status: str = 'sent', error_message: Optional[str] = None) -> int:
    """Store a message in the database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                '''INSERT INTO messages (role, content, status, error_message, timestamp)
                   VALUES (?, ?, ?, ?, ?)''',
                (role, content, status, error_message, datetime.now(timezone.utc))
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"Failed to store message: {e}")
        raise

# Routes
@app.route('/')
def home():
    """Render the chat interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/send_message', methods=['POST'])
@rate_limit
def send_message():
    """Handle message sending with proper error handling and validation"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        user_message = validate_message(data['message'])
        message_id = store_message('user', user_message)

        try:
            grok_response = make_grok_request(user_message)
            store_message('assistant', grok_response)
            return jsonify({
                'message': grok_response,
                'id': message_id,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })

        except ValueError as e:
            # Update the message status to error
            with get_db_connection() as conn:
                conn.execute(
                    'UPDATE messages SET status = ?, error_message = ? WHERE id = ?',
                    ('error', str(e), message_id)
                )
                conn.commit()
            return jsonify({'error': str(e)}), 400

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/get_history')
def get_history():
    """Retrieve chat history"""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                'SELECT role, content, timestamp, status FROM messages ORDER BY timestamp'
            )
            messages = [
                {
                    'role': row['role'],
                    'content': row['content'],
                    'timestamp': row['timestamp'],
                    'status': row['status']
                }
                for row in cursor.fetchall()
            ]
        return jsonify(messages)
    except sqlite3.Error as e:
        logger.error(f"Failed to retrieve chat history: {e}")
        return jsonify({'error': 'Failed to retrieve chat history'}), 500

@app.route('/retry_message/<int:message_id>', methods=['POST'])
@rate_limit
def retry_message(message_id):
    """Retry failed messages"""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                'SELECT content FROM messages WHERE id = ? AND status = ?',
                (message_id, 'error')
            )
            message = cursor.fetchone()

            if not message:
                return jsonify({'error': 'Message not found or not in error state'}), 404

            grok_response = make_grok_request(message['content'])
            store_message('assistant', grok_response)

            # Update original message status
            conn.execute(
                'UPDATE messages SET status = ?, retry_count = retry_count + 1 WHERE id = ?',
                ('sent', message_id)
            )
            conn.commit()

            return jsonify({'message': grok_response})

    except Exception as e:
        logger.error(f"Error retrying message: {e}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded'}), 429

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

# HTML Template with corrected JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grok Terminal</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&display=swap">
    <style>
        /* Base styles */
        body {
            font-family: 'Fira Code', monospace;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #0a0a0a;
            color: #00ff00;
        }

        .chat-container {
            width: 90%;
            max-width: 1000px;
            height: 90vh;
            border: 1px solid #1a1a1a;
            border-radius: 4px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            background-color: #0f0f0f;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.1);
        }

        .chat-header {
            background-color: #1a1a1a;
            padding: 10px 20px;
            border-bottom: 1px solid #2a2a2a;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chat-header h1 {
            margin: 0;
            font-size: 1.2em;
            color: #00ff00;
        }

        .status-container {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .connection-status {
            font-size: 0.8em;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #00ff00;
            transition: background-color 0.3s ease;
        }

        .status-indicator.offline {
            background-color: #ff0000;
        }

        .chat-messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 20px;
            scrollbar-width: thin;
            scrollbar-color: #00ff00 #1a1a1a;
        }

        .message {
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 3px;
            max-width: 80%;
            font-size: 0.9em;
            position: relative;
            line-height: 1.4;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .user-message {
            background-color: #1a1a1a;
            border-left: 3px solid #00ff00;
            margin-left: auto;
            color: #00ff00;
        }

        .bot-message {
            background-color: #141414;
            border-left: 3px solid #008f11;
            color: #008f11;
        }

        .message.error {
            border-left-color: #ff0000;
        }

        .message.loading {
            opacity: 0.7;
        }

        .retry-button {
            background-color: #1a1a1a;
            color: #ff0000;
            border: 1px solid #ff0000;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 0.8em;
            margin-top: 5px;
        }

        .retry-button:hover {
            background-color: #ff0000;
            color: #1a1a1a;
        }

        .code-block {
            background-color: #1a1a1a;
            border-radius: 4px;
            padding: 12px;
            margin: 8px 0;
            position: relative;
            font-family: 'Fira Code', monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-x: auto;
        }

        .copy-button {
            position: absolute;
            right: 10px;
            top: 10px;
            background-color: #2a2a2a;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 3px;
            padding: 5px 10px;
            font-size: 0.8em;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .code-block:hover .copy-button {
            opacity: 1;
        }

        .input-area {
            display: flex;
            padding: 20px;
            background-color: #1a1a1a;
            border-top: 1px solid #2a2a2a;
            position: relative;
        }

        #user-input {
            flex-grow: 1;
            padding: 12px;
            background-color: #0f0f0f;
            border: 1px solid #2a2a2a;
            border-radius: 3px;
            color: #00ff00;
            font-family: 'Fira Code', monospace;
            resize: none;
            min-height: 20px;
            max-height: 150px;
        }

        #user-input:focus {
            outline: none;
            border-color: #00ff00;
            box-shadow: 0 0 5px rgba(0, 255, 0, 0.3);
        }

        .char-counter {
            position: absolute;
            right: 90px;
            bottom: 25px;
            font-size: 0.8em;
            color: #666;
        }

        .char-counter.limit {
            color: #ff0000;
        }

        #send-button {
            padding: 12px 25px;
            background-color: #0f0f0f;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 3px;
            margin-left: 10px;
            cursor: pointer;
            font-family: 'Fira Code', monospace;
            transition: all 0.3s ease;
        }

        #send-button:hover:not(:disabled) {
            background-color: #00ff00;
            color: #0f0f0f;
        }

        #send-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .typing-indicator {
            padding: 10px;
            font-size: 0.8em;
            color: #666;
            font-style: italic;
        }

        .export-button {
            background: none;
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 0.8em;
        }

        .export-button:hover {
            background-color: #00ff00;
            color: #0f0f0f;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>GROK TERMINAL v1.0</h1>
            <div class="status-container">
                <button class="export-button" onclick="exportChat()">Export Chat</button>
                <div class="connection-status">
                    <div class="status-indicator"></div>
                    <span class="status-text">Connected</span>
                </div>
            </div>
        </div>
        <div id="chat-messages" class="chat-messages"></div>
        <div class="input-area">
            <textarea 
                id="user-input" 
                placeholder="Enter message..." 
                maxlength="4000"
                rows="1"
            ></textarea>
            <div class="char-counter">0/4000</div>
            <button id="send-button" disabled>SEND</button>
        </div>
    </div>
    <script>
        const chatMessages = document.getElementById('chat-messages');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        const charCounter = document.querySelector('.char-counter');
        const connectionIndicator = document.querySelector('.status-indicator');
        const connectionText = document.querySelector('.status-text');

        let isOnline = navigator.onLine;
        let isLoading = false;

        // Connection status handling
        function updateConnectionStatus() {
            isOnline = navigator.onLine;
            connectionIndicator.classList.toggle('offline', !isOnline);
            connectionText.textContent = isOnline ? 'Connected' : 'Offline';
            sendButton.disabled = !isOnline || !userInput.value.trim() || isLoading;
        }

        window.addEventListener('online', updateConnectionStatus);
        window.addEventListener('offline', updateConnectionStatus);

        // Message handling functions
        function formatTimestamp(timestamp) {
            return new Date(timestamp).toLocaleString();
        }

        function createMessageElement(role, content, timestamp, status = 'sent') {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', role === 'user' ? 'user-message' : 'bot-message');

            if (status === 'error') {
                messageDiv.classList.add('error');
            }

            const contentDiv = document.createElement('div');
            contentDiv.classList.add('message-content');

            if (role === 'assistant') {
                contentDiv.appendChild(formatCodeBlocks(content));
            } else {
                contentDiv.textContent = content;
            }

            messageDiv.appendChild(contentDiv);

            const timestampDiv = document.createElement('div');
            timestampDiv.classList.add('timestamp');
            timestampDiv.textContent = formatTimestamp(timestamp);
            messageDiv.appendChild(timestampDiv);

            if (status === 'error') {
                const retryButton = document.createElement('button');
                retryButton.classList.add('retry-button');
                retryButton.textContent = 'Retry';
                retryButton.onclick = () => retryMessage(messageDiv.dataset.messageId);
                messageDiv.appendChild(retryButton);
            }

            return messageDiv;
        }

        function formatCodeBlocks(content) {
            const container = document.createElement('div');
            const parts = content.split('```');

            for (let i = 0; i < parts.length; i++) {
                if (i % 2 === 0) {
                    if (parts[i].trim()) {
                        const textNode = document.createElement('div');
                        textNode.textContent = parts[i];
                        container.appendChild(textNode);
                    }
                } else {
                    const codeBlock = document.createElement('div');
                    codeBlock.classList.add('code-block');

                    const language = parts[i].split('\n')[0].trim();
                    const code = parts[i].slice(language.length).trim();

                    codeBlock.textContent = code;

                    const copyButton = document.createElement('button');
                    copyButton.classList.add('copy-button');
                    copyButton.textContent = 'Copy';
                    copyButton.onclick = () => {
                        navigator.clipboard.writeText(code);
                        copyButton.textContent = 'Copied!';
                        setTimeout(() => {
                            copyButton.textContent = 'Copy';
                        }, 2000);
                    };

                    codeBlock.appendChild(copyButton);
                    container.appendChild(codeBlock);
                }
            }

            return container;
        }

        // Chat functionality
        async function sendMessage() {
            if (isLoading || !isOnline) return;

            const message = userInput.value.trim();
            if (!message) return;

            try {
                isLoading = true;
                sendButton.disabled = true;
                userInput.disabled = true;

                // Create and append user message immediately
                const userMessageElement = createMessageElement('user', message, new Date());
                chatMessages.appendChild(userMessageElement);
                chatMessages.scrollTop = chatMessages.scrollHeight;

                // Clear input and update counter
                userInput.value = '';
                updateCharCounter();
                adjustTextareaHeight();

                // Show loading message
                const loadingMessage = createLoadingMessage();
                chatMessages.appendChild(loadingMessage);

                // Make the API call
                const response = await fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ message })
                });

                // Remove loading message
                if (loadingMessage.parentNode) {
                    chatMessages.removeChild(loadingMessage);
                }

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Failed to send message');
                }

                // Create and append bot response
                const botMessage = createMessageElement('assistant', data.message, new Date());
                chatMessages.appendChild(botMessage);

            } catch (error) {
                console.error('Error sending message:', error);
                const errorMessage = createMessageElement(
                    'assistant',
                    `Error: ${error.message}`,
                    new Date(),
                    'error'
                );
                chatMessages.appendChild(errorMessage);
            } finally {
                isLoading = false;
                sendButton.disabled = false;
                userInput.disabled = false;
                userInput.focus();
                chatMessages.scrollTop = chatMessages.scrollHeight;
                updateCharCounter();
            }
        }

        function createLoadingMessage() {
            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('message', 'bot-message', 'loading');
            loadingDiv.textContent = 'Thinking...';
            return loadingDiv;
        }

        async function retryMessage(messageId) {
            if (!messageId || isLoading) return;

            try {
                isLoading = true;
                const response = await fetch(`/retry_message/${messageId}`, {
                    method: 'POST'
                });

                if (!response.ok) {
                    throw new Error(await response.text());
                }

                const data = await response.json();
                const botMessage = createMessageElement('assistant', data.message, new Date());
                chatMessages.appendChild(botMessage);

            } catch (error) {
                console.error('Retry failed:', error);
            } finally {
                isLoading = false;
            }
        }

        function exportChat() {
            try {
                const messages = Array.from(chatMessages.children).map(msg => {
                    const content = msg.querySelector('.message-content').textContent;
                    const timestamp = msg.querySelector('.timestamp').textContent;
                    const isUser = msg.classList.contains('user-message');
                    return `[${timestamp}] ${isUser ? 'User' : 'Grok'}: ${content}`;
                });

                const chatText = messages.join('\n\n');
                const blob = new Blob([chatText], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `chat_export_${new Date().toISOString().split('T')[0]}.txt`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } catch (error) {
                console.error('Export failed:', error);
            }
        }

        async function loadChatHistory() {
            try {
                const response = await fetch('/get_history');
                if (!response.ok) throw new Error('Failed to load chat history');

                const messages = await response.json();
                chatMessages.innerHTML = '';

                messages.forEach(msg => {
                    const messageElement = createMessageElement(
                        msg.role,
                        msg.content,
                        msg.timestamp,
                        msg.status
                    );
                    chatMessages.appendChild(messageElement);
                });

                chatMessages.scrollTop = chatMessages.scrollHeight;
            } catch (error) {
                console.error('Failed to load chat history:', error);
            }
        }

        // Utility functions
        function updateCharCounter() {
            const length = userInput.value.length;
            const counter = document.querySelector('.char-counter');
            if (counter) {
                counter.textContent = `${length}/4000`;
                counter.classList.toggle('limit', length >= 4000);
            }
            sendButton.disabled = length === 0 || length > 4000 || isLoading || !isOnline;
        }

        function adjustTextareaHeight() {
            userInput.style.height = 'auto';
            userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
        }

        // Event listeners
        document.addEventListener('DOMContentLoaded', () => {
            userInput.addEventListener('input', () => {
                updateCharCounter();
                adjustTextareaHeight();
            });

            sendButton.addEventListener('click', (e) => {
                e.preventDefault();
                sendMessage();
            });

            userInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            loadChatHistory();
            updateConnectionStatus();
            updateCharCounter();

            // Restore any unsent messages from localStorage
            const draftMessage = localStorage.getItem('draftMessage');
            if (draftMessage) {
                userInput.value = draftMessage;
                updateCharCounter();
                adjustTextareaHeight();
            }
        });

        // Save draft messages
        window.addEventListener('beforeunload', () => {
            localStorage.setItem('draftMessage', userInput.value);
        });

        // Handle visibility change
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                loadChatHistory();
                updateConnectionStatus();
            }
        });

        // Periodic connection check
        setInterval(() => {
            fetch('/ping')
                .then(() => {
                    if (!isOnline) {
                        isOnline = true;
                        updateConnectionStatus();
                    }
                })
                .catch(() => {
                    if (isOnline) {
                        isOnline = false;
                        updateConnectionStatus();
                    }
                });
        }, 30000);
    </script>
</body>
</html>
'''

# Add the `/ping` route
@app.route('/ping')
def ping():
    """Simple endpoint to check if server is alive"""
    return jsonify({'status': 'ok'})

# Log request and response
@app.before_request
def log_request_info():
    """Log details about each request"""
    logger.info('Headers: %s', request.headers)
    logger.info('Body: %s', request.get_data())

@app.after_request
def log_response_info(response):
    """Log details about each response"""
    logger.info('Response Status: %s', response.status)
    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))