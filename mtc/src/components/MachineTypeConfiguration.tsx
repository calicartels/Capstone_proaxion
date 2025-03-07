import { useState, useContext } from 'react';
import MTCInput from './MTCInput.tsx';
import ChatBot from './ChatBot.tsx';
import VideoPlayer from './VideoPlayer.tsx'; // New component
import { MachineContext, MachineContextProvider } from '../context/MachineContext.tsx'; // New context
import './MachineTypeConfiguration.css';

interface MachineTypeConfigurationProps {
  onHomeClick: () => void;
}

function MachineTypeConfiguration({ onHomeClick }: MachineTypeConfigurationProps) {
  const [step, setStep] = useState(1);
  const [activeButton, setActiveButton] = useState<string | null>(null);
  const { setMachineType, setTransmissionType } = useContext(MachineContext);

  const handleMachineTypeChange = (value: string) => {
    setMachineType(value);
  };

  const handleTransmissionTypeChange = (value: string) => {
    setTransmissionType(value);
  };

  const handleNextClick = () => {
    setActiveButton('next');
    setStep(step + 1);
  };

  const handleBackClick = () => {
    setActiveButton('back');
    if (step === 1) {
      onHomeClick();
    } else {
      setStep(step - 1);
    }
  };

  const step1Options = [
    { value: 'Fan', label: 'Fan' },
    { value: 'Other', label: 'Other' },
  ];

  const step2Options = [
    { value: 'Belt-Driven', label: 'Belt-Driven' },
    { value: 'Direct Drive', label: 'Direct Drive' },
  ];

  return (
    <MachineContextProvider>
      <div className="machine-type-configuration-container">
        <h1>Install New Sensors</h1>
        <div className="machine-type-configuration">
          {step === 1 && (
            <MTCInput 
              title="Type of Machine" 
              options={step1Options}
              onChange={handleMachineTypeChange}
            />
          )}
          {step === 2 && (
            <MTCInput 
              title="Power Transmission" 
              options={step2Options}
              onChange={handleTransmissionTypeChange}
            />
          )}
          {step === 3 && (
            <div className="instructions-chatbot-container">
              <div className="instructions">
                <VideoPlayer />
              </div>
              <div className="chatbot">
                <ChatBot />
              </div>
            </div>
          )}
          <div className="footer-buttons">
            {step === 1 ? (
              <button 
                onClick={onHomeClick} 
                className={activeButton === 'home' ? 'active' : ''}
              >
                Home
              </button>
            ) : (
              <button 
                onClick={handleBackClick} 
                className={activeButton === 'back' ? 'active' : ''}
              >
                Back
              </button>
            )}
            {step < 3 ? (
              <button 
                onClick={handleNextClick} 
                className={activeButton === 'next' ? 'active' : ''}
              >
                Next
              </button>
            ) : (
              <button 
                onClick={onHomeClick} 
                className={activeButton === 'home' ? 'active' : ''}
              >
                Home
              </button>
            )}
          </div>
        </div>
      </div>
    </MachineContextProvider>
  );
}

export default MachineTypeConfiguration;