# React API Integration Guide

## Backend Setup

1. **Start the FastAPI server:**
```bash
# In your portfolio-backend directory
python main.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Server will run on:** `http://localhost:8000`

## React Integration

### 1. Environment Setup

Add to your React project's `.env` file:
```env
REACT_APP_API_URL=http://localhost:8000
```

### 2. API Service Component

Create `src/services/api.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  async chat(message) {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to send message');
      }
      
      const data = await response.json();
      return data.reply;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/`);
      const data = await response.json();
      return data.status === 'running';
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

export default new ApiService();
```

### 3. React Hook for Chat

Create `src/hooks/useChat.js`:
```javascript
import { useState, useCallback } from 'react';
import apiService from '../services/api';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (userMessage) => {
    if (!userMessage.trim()) return;

    // Add user message
    const newUserMessage = { text: userMessage, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, newUserMessage]);
    
    setIsLoading(true);
    setError(null);

    try {
      const reply = await apiService.chat(userMessage);
      const botMessage = { 
        text: reply, 
        sender: 'bot', 
        timestamp: new Date() 
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError(err.message);
      // Add error message
      const errorMessage = { 
        text: 'Sorry, I encountered an error. Please try again.', 
        sender: 'bot', 
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
  };
};
```

### 4. Chat Component Example

Create `src/components/ChatComponent.jsx`:
```jsx
import React, { useState, useRef, useEffect } from 'react';
import { useChat } from '../hooks/useChat';

const ChatComponent = () => {
  const { messages, isLoading, error, sendMessage } = useChat();
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;
    
    const message = inputValue;
    setInputValue('');
    await sendMessage(message);
  };

  return (
    <div className="chat-container">
      <div className="messages-container">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
          >
            <div className="message-content">
              {message.text}
            </div>
            <div className="message-time">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
          className="message-input"
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          className="send-button"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatComponent;
```

### 5. CSS Styling

Add to your CSS file:
```css
.chat-container {
  max-width: 600px;
  height: 500px;
  border: 1px solid #ddd;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  margin: 20px auto;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f9f9f9;
}

.message {
  margin-bottom: 15px;
  max-width: 80%;
}

.message.user {
  margin-left: auto;
  background: #007bff;
  color: white;
  padding: 10px 15px;
  border-radius: 18px 18px 4px 18px;
}

.message.bot {
  margin-right: auto;
  background: white;
  border: 1px solid #e0e0e0;
  padding: 10px 15px;
  border-radius: 18px 18px 18px 4px;
}

.message.error {
  background: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}

.message-time {
  font-size: 0.75em;
  opacity: 0.7;
  margin-top: 5px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 10px 15px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #999;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.input-form {
  display: flex;
  padding: 15px;
  border-top: 1px solid #ddd;
  background: white;
}

.message-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.send-button {
  margin-left: 10px;
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.send-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  padding: 10px;
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  margin: 10px;
  border-radius: 4px;
}
```

### 6. Usage in Your App

```jsx
import React from 'react';
import ChatComponent from './components/ChatComponent';

function App() {
  return (
    <div className="App">
      <h1>AI Assistant Chat</h1>
      <ChatComponent />
    </div>
  );
}

export default App;
```

## Important Notes

1. **CORS is already configured** in your FastAPI backend for `localhost:3000`
2. **Environment variables** - Make sure to create `.env` file in your React project
3. **Error handling** - The integration includes comprehensive error handling
4. **Loading states** - Visual feedback during API calls
5. **Message history** - Maintains chat conversation state

## Testing

1. Start both servers:
   - Backend: `python main.py` (port 8000)
   - Frontend: `npm start` (port 3000)

2. Open browser and test the chat functionality

3. Check browser console for any API errors
