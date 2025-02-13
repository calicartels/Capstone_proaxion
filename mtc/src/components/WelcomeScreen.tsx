import './WelcomeScreen.css';

interface WelcomeScreenProps {
  onHomeClick: () => void;
  onMachineTypeConfigurationClick: () => void;
  onMachineHealthClick: () => void;
}

export default function WelcomeScreen( { onMachineTypeConfigurationClick, onMachineHealthClick }: WelcomeScreenProps ) {
  return (
      <div className="welcome-screen">
        <h1>Your Personal Machine Assistant</h1>
        <div className="button-container">
          <button onClick={onMachineTypeConfigurationClick}>Machine Type Configuration</button>
          <button onClick={onMachineHealthClick}>Machine Health</button>
        </div>
      </div>
  );
}