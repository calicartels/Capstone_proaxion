import React, { useState } from 'react';
import './WelcomeScreen.css';
import ContactUs from './ContactUs';
import ChangeSensor from './change_sensor/ChangeSensor';
import ChangeMachinePart from './change_machine_part/ChangeMachinePart'; // Import ChangeMachinePart

interface WelcomeScreenProps {
  onHomeClick: () => void;
  onMachineTypeConfigurationClick: () => void;
  onMachineHealthClick: () => void;
  onEnhanceSensorInstallsClick: () => void;
  onOptimizeMachineDataClick: () => void;
  onCreateMaintenancePlanClick: () => void;
  onChangeSensorClick: () => void;
}

export default function WelcomeScreen({
  onHomeClick,
  onMachineTypeConfigurationClick,
  onMachineHealthClick,
  onEnhanceSensorInstallsClick,
  onOptimizeMachineDataClick,
  onCreateMaintenancePlanClick,
  onChangeSensorClick,
}: WelcomeScreenProps) {
  const [showContactUs, setShowContactUs] = useState(false);
  const [showChangeSensor, setShowChangeSensor] = useState(false);
  const [showChangeMachinePart, setShowChangeMachinePart] = useState(false); // Add state for ChangeMachinePart

  const handleContactUsClick = () => {
    setShowContactUs(true);
  };

  const handleBackClick = () => {
    setShowContactUs(false);
    setShowChangeSensor(false);
    setShowChangeMachinePart(false); // Reset ChangeMachinePart state when navigating back
  };

  const handleHomeClick = () => {
    setShowContactUs(false);
    setShowChangeSensor(false);
    setShowChangeMachinePart(false); // Ensure all states are reset to show WelcomeScreen
  };

  const handleChangeSensorClick = () => {
    setShowChangeSensor(true);
  };

  const handleCreateMaintenancePlanClick = () => {
    setShowChangeMachinePart(true); // Show ChangeMachinePart component
  };

  const handleChangeMachineComponentClick = () => {
    setShowChangeMachinePart(true); // Show ChangeMachinePart component
  };

  if (showContactUs) {
    return <ContactUs onBackClick={handleBackClick} />;
  }

  if (showChangeSensor) {
    return <ChangeSensor onHomeClick={handleHomeClick} />; // Pass handleHomeClick to ChangeSensor
  }

  if (showChangeMachinePart) {
    return <ChangeMachinePart onHomeClick={handleHomeClick} />; // Pass handleHomeClick to ChangeMachinePart
  }

  return (
    <div className="welcome-screen">
      <h1>Your Personal Machine Assistant</h1>
      <div className="button-container">
        <button onClick={onMachineTypeConfigurationClick}>Monitor a New Machine</button>
        <button onClick={onMachineHealthClick}>Trouble Shoot a Machine</button>
      </div>
      <div className="button-container">
        <button onClick={onEnhanceSensorInstallsClick}>Update an Existing Machine</button>
        <button onClick={onOptimizeMachineDataClick}>Add Machine Data</button>
      </div>
      <div className="button-container">
        <button onClick={handleChangeSensorClick}>Change a Sensor</button>
        <button onClick={handleChangeMachineComponentClick}>Change a Machine Component</button>
        
      </div>
      <div className="button-container">
      <button onClick={handleCreateMaintenancePlanClick}>Create a Maintenance Plan</button>
        <button onClick={handleContactUsClick}>Contact Us</button>
      </div>
    </div>
  );
}