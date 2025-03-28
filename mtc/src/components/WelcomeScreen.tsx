import React, { useState } from 'react';
import './WelcomeScreen.css';
import ContactUs from './ContactUs';
import ChangeSensor from './change_sensor/ChangeSensor';

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
  const [showChangeSensor, setShowChangeSensor] = useState(false); // Add state for ChangeSensor

  const handleContactUsClick = () => {
    setShowContactUs(true);
  };

  const handleBackClick = () => {
    setShowContactUs(false);
    setShowChangeSensor(false); // Reset ChangeSensor state when navigating back
  };

  const handleChangeSensorClick = () => {
    setShowChangeSensor(true); // Show ChangeSensor component
  };

  if (showContactUs) {
    return <ContactUs onBackClick={handleBackClick} />;
  }

  if (showChangeSensor) {
    return <ChangeSensor onHomeClick={handleBackClick} />; // Render ChangeSensor component
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
        <button onClick={handleChangeSensorClick}>Change a Sensor</button> {/* Update button to use local handler */}
        <button onClick={onCreateMaintenancePlanClick}>Create a Maintenance Plan</button>
      </div>
      <div className="button-container">
        <button>Change a Machine Component</button>
        <button onClick={handleContactUsClick}>Contact Us</button>
      </div>
    </div>
  );
}