import React, { useState, useEffect } from 'react';
import ChatBotInput from './ChatBotInput';
import './ChatBot.css';

interface Message {
  text: string;
  sender: 'user' | 'bot';
  sources?: Array<{ id: string; title: string }>;
}

const ChatBot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [initialMessage, setInitialMessage] = useState(true);

  // Fetch context from current screen when component mounts
  useEffect(() => {
    if (initialMessage) {
      handleContextUpdate("Tell me about installing sensors for a fan");
      setInitialMessage(false);
    }
  }, [initialMessage]);

  const handleContextUpdate = async (context: string) => {
    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: context }),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      
      // Add bot response to chat
      setMessages([{
        text: data.text,
        sender: 'bot',
        sources: data.sources
      }]);
    } catch (error) {
      console.error('Error updating context:', error);
      setMessages([{
        text: 'I encountered an error while retrieving information. Please try again.',
        sender: 'bot'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (message: string) => {
    // Add user message to chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, sender: 'user' },
    ]);
    
    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      
      // Add bot response to chat
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: data.text,
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
            {message.text}
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
      </div>
      <ChatBotInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatBot;