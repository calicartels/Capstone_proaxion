import React, { useState, useEffect, useRef, useContext } from 'react';
import ChatBotInput from './ChatBotInput';
import './ChatBot.css';
import ReactMarkdown from 'react-markdown';
import { MachineContext } from '../context/MachineContext';
import { installationSteps } from './VideoPlayer';
import instructionsData from '../data/instructions.json';

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
  
  // Access machine context
  const { 
    machineType, 
    transmissionType, 
    currentInstallationStep,
    setCurrentInstallationStep 
  } = useContext(MachineContext);

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
      // Customized welcome message based on machine type
      const welcomeMessage = `Hello! I'm ProAxion Assistant, here to help you with ${machineType} sensor installation. I see you're working with a ${transmissionType} system. How can I assist you today?`;
      
      setMessages([{
        text: welcomeMessage,
        sender: 'bot'
      }]);
      setInitialPromptSent(true);
    }
  }, [initialPromptSent, machineType, transmissionType]);

  // Detect installation-related queries and advance installation step
  const detectInstallationIntent = (message: string): number | null => {
    const lowercaseMessage = message.toLowerCase();
    
    // Check for general installation intents
    if (
      lowercaseMessage.includes('help with installation') || 
      lowercaseMessage.includes('begin installation') ||
      lowercaseMessage.includes('install the sensor') ||
      lowercaseMessage.includes('guide me through') ||
      lowercaseMessage.includes('need help with the installation')
    ) {
      return 0; // Start from the first step (Materials Required)
    }
    
    // Check for step-specific intents
    for (let i = 0; i < installationSteps.length; i++) {
      const step = installationSteps[i];
      for (const trigger of step.promptTriggers) {
        if (lowercaseMessage.includes(trigger)) {
          return i;
        }
      }
    }
    
    // Check for "next step" or "continue" type requests
    if (
      lowercaseMessage.includes('next step') || 
      lowercaseMessage.includes('continue') ||
      lowercaseMessage.includes('what\'s next') ||
      lowercaseMessage.includes('what now') ||
      lowercaseMessage.includes('how do i') ||
      lowercaseMessage.includes('go on')
    ) {
      return currentInstallationStep + 1 < installationSteps.length 
        ? currentInstallationStep + 1 
        : null;
    }
    
    return null;
  };

  // Enhanced function to detect step-specific questions
  const detectStepQuestion = (message: string): number | null => {
    const lowercaseMessage = message.toLowerCase();
    
    // Check for specific step mentions
    if (lowercaseMessage.includes('step 1') || lowercaseMessage.includes('first step')) {
      return 1;
    } else if (lowercaseMessage.includes('step 2') || lowercaseMessage.includes('second step')) {
      return 2;
    } else if (lowercaseMessage.includes('step 3') || lowercaseMessage.includes('third step')) {
      return 3;
    } else if (lowercaseMessage.includes('step 4') || lowercaseMessage.includes('fourth step')) {
      return 4;
    } else if (lowercaseMessage.includes('step 5') || lowercaseMessage.includes('fifth step')) {
      return 5;
    } else if (lowercaseMessage.includes('step 6') || lowercaseMessage.includes('sixth step')) {
      return 6;
    } else if (lowercaseMessage.includes('step 7') || lowercaseMessage.includes('seventh step')) {
      return 7;
    }
    
    // Check for content-based matches
    for (let i = 1; i < instructionsData.length; i++) {
      const stepData = instructionsData[i];
      
      // Check if question contains keywords from this step
      for (const section of stepData.content) {
        const sectionText = section.text.join(' ').toLowerCase();
        const sectionKeywords = sectionText.split(' ')
          .filter(word => word.length > 4)  // Only consider longer words as keywords
          .map(word => word.replace(/[.,?!;:]/g, ''));  // Remove punctuation
          
        const matchCount = sectionKeywords.filter(keyword => 
          lowercaseMessage.includes(keyword)).length;
          
        // If question matches several keywords from this step, it's likely about this step
        if (matchCount >= 3) {
          return i;
        }
      }
    }
    
    // If no specific step is detected, return the current step as context
    return null;
  };

  const handleSendMessage = async (message: string) => {
    // Add user message to chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, sender: 'user' },
    ]);
    
    // Check for installation intent
    const detectedStep = detectInstallationIntent(message);
    
    // Check for step-specific questions
    const questionStep = detectStepQuestion(message);
  
    if (detectedStep === 0 && message.toLowerCase().includes('help with the installation')) {
      // Starting the installation guide
      setCurrentInstallationStep(0);
      
      // Add a more detailed installation guide introduction
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: "I'll guide you through the sensor installation step by step. Let's start with gathering the materials you'll need. I'll show each step in the video as we go through the process. Let me know when you're ready to move to the next step!",
          sender: 'bot'
        },
        {
          text: `**Step 1: Materials Required**\n\nFor this installation, you'll need:\n- Indent tool or small drill\n- Spot-face tool\n- ¼"-28 thread tap\n- Thread locker (Vibra-Tite® Blue recommended)\n- Silicone sealant\n- 1/8" hex key\n\nDo you have all these materials ready?`,
          sender: 'bot'
        },
      ]);
      
      return; // Skip API call
    } else if (detectedStep !== null && detectedStep < installationSteps.length) {
      setCurrentInstallationStep(detectedStep);
      
      // Add bot response for this installation step
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: installationSteps[detectedStep].instruction,
          sender: 'bot'
        },
      ]);
      
      return; // Skip API call
    } else if (questionStep !== null && questionStep < instructionsData.length) {
      // Answer questions about specific installation steps
      const stepData = instructionsData[questionStep];
      
      // Format a response based on the instruction step data
      let responseText = `**About ${stepData.title}:**\n\n`;
      
      // Add each content section
      stepData.content.forEach(section => {
        if (section.subtitle) {
          responseText += `**${section.subtitle}**\n`;
        }
        
        section.text.forEach(paragraph => {
          responseText += `${paragraph}\n\n`;
        });
      });
      
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: responseText,
          sender: 'bot'
        },
      ]);
      
      // Update the current installation step to match the question
      setCurrentInstallationStep(questionStep);
      
      return; // Skip API call
    }
    
    setIsLoading(true);
    
    try {
      console.log("Sending message to API:", message);
      console.log("With machine context:", { machineType, transmissionType });
      
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message,
          history: conversationHistory,
          machineContext: {
            machineType,
            transmissionType
          }
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