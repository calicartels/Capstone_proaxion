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
  const [activeButton, setActiveButton] = useState<string | null>(null);
  const [machineType, setMachineType] = useState<string>(""); // New state for Type of Machine
  const [powerTransmission, setPowerTransmission] = useState<string>(""); // Capture Power Transmission
  const [fanOverhung, setFanOverhung] = useState<string>(""); // Already present
  const [horsepower, setHorsepower] = useState<string>("");
  const [installationMethod, setInstallationMethod] = useState<string>("");

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
    { value: 'MT1', label: 'Fan' },
    { value: 'MT2', label: 'Other' },
  ];

  const step2Options = [
    { value: 'PT1', label: 'Belt-Driven' },
    { value: 'PT2', label: 'Direct Drive' },
  ];

  const installationOptions = [
    { value: 'DrillTap', label: 'Drill and Tap (preferred)' },
    { value: 'Epoxy', label: 'Epoxy Adhesive' },
    { value: 'LiftingLug', label: 'Lifting Lug' },
    { value: 'FinMount', label: 'Fin Mount' },
    { value: 'Magnet', label: 'Magnet (not preferred)' },
  ];

  return (
    <div className="machine-type-configuration-container">
      <h1>Monitor a New Machine</h1>
      <div className="machine-type-configuration">
        {step === 1 && (
          <MTCInput 
            title="Type of Machine" 
            options={step1Options} 
            value={machineType}
            onChange={(e) => setMachineType(e.target.value)}
          />
        )}
        {step === 2 && (
          <MTCInput 
            title="Power Transmission" 
            options={step2Options} 
            value={powerTransmission}
            onChange={(e) => setPowerTransmission(e.target.value)}
          />
        )}
        {step === 3 && (
          <MTCInput 
            title="Is the Fan Overhung?" 
            options={[
              { value: 'no', label: 'No' },
              { value: 'yes', label: 'Yes' }
            ]}
            value={fanOverhung}
            onChange={(e) => setFanOverhung(e.target.value)}
          />
        )}
        {step === 4 && (
          <div className="horsepower-input-container">
            <h2>Horsepower</h2>
            <input 
              id="horsepower" 
              type="number" 
              placeholder="Enter horsepower" 
              value={horsepower}
              onChange={(e) => setHorsepower(e.target.value)}
              className="horsepower-input"
            />
          </div>
        )}
        {step === 5 && (
          <MTCInput
            title="Installation Method"
            options={installationOptions}
            value={installationMethod}
            onChange={(e) => setInstallationMethod(e.target.value)}
          />
        )}
        {step === 6 && (
          <div className="instructions-chatbot-container">
            <div className="instructions">
              <MTCInstructions 
                userSelections={{
                  machineType,
                  powerTransmission,
                  fanOverhung,
                  horsepower,
                  installationMethod
                }}
              />
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
          {step < 6 ? (
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
  );
}

export default MachineTypeConfiguration;