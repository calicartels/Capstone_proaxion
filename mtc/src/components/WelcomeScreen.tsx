import React, { useState } from 'react';
import './WelcomeScreen.css';
import ContactUs from './ContactUs';

interface WelcomeScreenProps {
  onHomeClick: () => void;
  onMachineTypeConfigurationClick: () => void;
  onMachineHealthClick: () => void;
  onEnhanceSensorInstallsClick: () => void;
  onOptimizeMachineDataClick: () => void;
  onCreateMaintenancePlanClick: () => void; // Add new prop here
}

export default function WelcomeScreen({
  onHomeClick,
  onMachineTypeConfigurationClick,
  onMachineHealthClick,
  onEnhanceSensorInstallsClick,
  onOptimizeMachineDataClick,
  onCreateMaintenancePlanClick, // Destructure new prop
}: WelcomeScreenProps) {
  const [showContactUs, setShowContactUs] = useState(false);

  const handleContactUsClick = () => {
    setShowContactUs(true);
  };

  const handleBackClick = () => {
    setShowContactUs(false);
  };

  if (showContactUs) {
    return <ContactUs onBackClick={handleBackClick} />;
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
        <button onClick={onCreateMaintenancePlanClick}>Create a Maintenance Plan</button>
        <button onClick={handleContactUsClick}>Contact Us</button>
      </div>
    </div>
  );
}