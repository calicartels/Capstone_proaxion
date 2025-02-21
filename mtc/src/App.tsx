import React, { useState } from 'react';
import WelcomeScreen from './components/WelcomeScreen';
import MachineTypeConfiguration from './components/MachineTypeConfiguration';
import MachineHealth from './components/MachineHealth';
import ContactUs from './components/ContactUs';
import './App.css';

function App() {
  const [currentScreen, setCurrentScreen] = useState('welcome');

  const handleHomeClick = () => {
    setCurrentScreen('welcome');
  };

  const handleMachineTypeConfigurationClick = () => {
    setCurrentScreen('machineTypeConfiguration');
  };

  const handleMachineHealthClick = () => {
    setCurrentScreen('machineHealth');
  };

  const handleContactUsClick = () => {
    setCurrentScreen('contact');
  };

  return (
    <div className="App">
      {currentScreen === 'welcome' && (
        <WelcomeScreen
          onHomeClick={handleHomeClick}
          onMachineTypeConfigurationClick={handleMachineTypeConfigurationClick}
          onMachineHealthClick={handleMachineHealthClick}
        />
      )}
      {currentScreen === 'machineTypeConfiguration' && (
        <MachineTypeConfiguration onHomeClick={handleHomeClick} />
      )}
      {currentScreen === 'machineHealth' && (
        <MachineHealth onHomeClick={handleHomeClick} />
      )}
      {currentScreen === 'contact' && <ContactUs onBackClick={handleHomeClick} />}
    </div>
  );
}

export default App;

