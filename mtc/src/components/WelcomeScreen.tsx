import './WelcomeScreen.css';

interface WelcomeScreenProps {
  onHomeClick: () => void;
  onMachineTypeConfigurationClick: () => void;
  onMachineHealthClick: () => void;
  onContactUsClick: () => void;
}

export default function WelcomeScreen( { onMachineTypeConfigurationClick, onMachineHealthClick, onContactUsClick }: WelcomeScreenProps ) {
  return (
      <div className="welcome-screen">
        <h1>Your Personal Machine Assistant</h1>
        <div className="button-container">
          <button onClick={onMachineTypeConfigurationClick}>Install New Sensors</button>
          <button onClick={onMachineHealthClick}>Trouble Shoot Machine</button>
        </div>
        <div className="button-container">
          <button>Enhance Sensor Installs</button>
          <button>Optimize Machine Data</button>
        </div>
        <div className="button-container centered">
          <button onClick={onContactUsClick}>Contact Us</button>
        </div>
      </div>
  );
}