import React, { useState } from 'react';
import './WelcomeScreen.css';
import ContactUs from './ContactUs';

interface WelcomeScreenProps {
  onHomeClick: () => void;
  onMachineTypeConfigurationClick: () => void;
  onMachineHealthClick: () => void;
  onEnhanceSensorInstallsClick: () => void;
  onOptimizeMachineDataClick: () => void;
}

export default function WelcomeScreen({
  onMachineTypeConfigurationClick,
  onMachineHealthClick,
  onEnhanceSensorInstallsClick,
  onOptimizeMachineDataClick,
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
        <button onClick={onMachineTypeConfigurationClick}>Install New Sensors</button>
        <button onClick={onMachineHealthClick}>Trouble Shoot Machine</button>
      </div>
      <div className="button-container">
        <button onClick={onEnhanceSensorInstallsClick}>Enhance Sensor Installs</button>
        <button onClick={onOptimizeMachineDataClick}>Optimize Machine Data</button>
      </div>
      <div className="button-container centered">
        <button onClick={handleContactUsClick}>Contact Us</button>
      </div>
    </div>
  );
}