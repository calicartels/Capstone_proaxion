import React, { useState, useEffect, useRef } from 'react';
import ChatBotInput from './ChatBotInput';
import './ChatBot.css';
import ReactMarkdown from 'react-markdown';

interface Message {
  text: string;
  sender: 'user' | 'bot';
  sources?: Array<{ id: string; title: string }>;
}

interface ConversationItem {
  role: 'user' | 'assistant';
  content: string;
}

const ChatBot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationHistory, setConversationHistory] = useState<ConversationItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [initialPromptSent, setInitialPromptSent] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Update conversation history when messages change
  useEffect(() => {
    const newHistory = messages.map(msg => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.text
    }));
    setConversationHistory(newHistory);
  }, [messages]);

  // Send initial welcome message on component mount
  useEffect(() => {
    if (!initialPromptSent) {
      const welcomeMessage = `Hello! I'm ProAxion Assistant. How can I assist you today?`;
      
      setMessages([{
        text: welcomeMessage,
        sender: 'bot'
      }]);
      setInitialPromptSent(true);
    }
  }, [initialPromptSent]);

  const handleSendMessage = async (message: string) => {
    // Add user message to chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, sender: 'user' },
    ]);

    setIsLoading(true);
    
    try {
      console.log("Sending message to API:", message);
      
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message,
          history: conversationHistory
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("Received response:", data);
      
      // Add bot response to chat
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: data.text || "I couldn't process that request. Could you try rephrasing your question?",
          sender: 'bot',
          sources: data.sources
        },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: 'I encountered an error while generating a response. Please try again.',
          sender: 'bot'
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <h2>ProAxion Assistant</h2>
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div key={index} className={`chatbot-message ${message.sender}`}>
            {message.sender === 'bot' ? (
              <ReactMarkdown>{message.text}</ReactMarkdown>
            ) : (
              <p>{message.text}</p>
            )}
            {message.sources && message.sources.length > 0 && (
              <div className="message-sources">
                <small>
                  Sources: {message.sources.map(s => s.title).join(', ')}
                </small>
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="loading-message">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <ChatBotInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatBot;