import React, { useState, useEffect, useRef } from 'react';
import { Send } from 'lucide-react';
import './ChatBotInput.css';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
}

const ChatBotInput: React.FC<ChatInputProps> = ({ onSendMessage }) => {
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  };

  return (
    <div className="chatbot-input-container">
      <form onSubmit={handleSubmit} className="flex w-full items-center space-x-2">
        <input
          ref={inputRef}
          type="text"
          className="chatbot-input"
          placeholder="Type a message..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
        <button type="submit" className="chatbot-send-button">
          <Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
};

export default ChatBotInput;