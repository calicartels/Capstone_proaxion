import { useState } from 'react';
import MTCInput from './MTCInput.tsx';
import MTCInstructions from './MTCInstructions.tsx';
import ChatBot from './ChatBot.tsx';
import './MachineTypeConfiguration.css';

interface MachineTypeConfigurationProps {
  onHomeClick: () => void;
}

function MachineTypeConfiguration({ onHomeClick }: MachineTypeConfigurationProps) {
  const [step, setStep] = useState(1);

  const handleNextClick = () => {
    setStep(step + 1);
  };

  const handleBackClick = () => {
    if (step === 1) {
      onHomeClick();
    } else {
      setStep(step - 1);
    }
  };

  const step1Options = [
    { value: 'MT1', label: 'Fan' },
    { value: 'MT2', label: 'Other' },
  ];

  const step2Options = [
    { value: 'PT1', label: 'Belt-Driven' },
    { value: 'PT2', label: 'Direct Drive' },
  ];

  return (
    <div className="machine-type-configuration-container">
      <h1>Machine Type Configuration</h1>
      <div className="machine-type-configuration">
        {step === 1 && (
          <MTCInput 
            onBackClick={handleBackClick} 
            onNextClick={handleNextClick}
            title="Type of Machine" 
            options={step1Options} 
          />
        )}
        {step === 2 && (
          <MTCInput 
            onBackClick={handleBackClick} 
            onNextClick={handleNextClick}
            title="Power Transmission" 
            options={step2Options} 
          />
        )}
        {step === 3 && (
          <div className="instructions-chatbot-container">
            <div className="instructions">
              <MTCInstructions />
            </div>
            <div className="chatbot">
              <ChatBot />
            </div>
            <div className="footer-buttons">
              <button onClick={handleBackClick}>Back</button>
              <button onClick={onHomeClick}>Home</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default MachineTypeConfiguration;