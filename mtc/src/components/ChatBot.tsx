import React, { useState } from 'react';
import ChatBotInput from './ChatBotInput';
import './ChatBot.css';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const ChatBot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSendMessage = (message: string) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, sender: 'user' },
      { text: "I'm here to help.", sender: 'bot' },
    ]);
  };

  return (
    <div className="chatbot-container">
      <h2>ChatBot</h2>
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div key={index} className={`chatbot-message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <ChatBotInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatBot;