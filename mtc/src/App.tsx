import React, { useState } from 'react';
import { FaBars } from 'react-icons/fa';
import WelcomeScreen from './components/WelcomeScreen';
import MachineTypeConfiguration from './components/MachineTypeConfiguration';
import MachineHealth from './components/MachineHealth';
import EnhanceSensorInstalls from './components/EnhanceSensorInstalls';
import OptimizeMachineData from './components/OptimizeMachineData';
import ContactUs from './components/ContactUs';
import { Sidebar } from './components/Sidebar';
import './App.css';
import ProAxionLogo from './assets/ProAxion-logo.png'; // Import the logo

function App() {
  const [currentScreen, setCurrentScreen] = useState('welcome');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleHomeClick = () => {
    setCurrentScreen('welcome');
    setIsSidebarOpen(false);
  };

  const handleMachineTypeConfigurationClick = () => {
    setCurrentScreen('machineTypeConfiguration');
    setIsSidebarOpen(false);
  };

  const handleMachineHealthClick = () => {
    setCurrentScreen('machineHealth');
    setIsSidebarOpen(false);
  };

  const handleEnhanceSensorInstallsClick = () => {
    setCurrentScreen('enhanceSensorInstalls');
    setIsSidebarOpen(false);
  };

  const handleOptimizeMachineDataClick = () => {
    setCurrentScreen('optimizeMachineData');
    setIsSidebarOpen(false);
  };

  const handleContactUsClick = () => {
    setCurrentScreen('contact');
    setIsSidebarOpen(false);
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="App">
      <header className="header">
        <img src={ProAxionLogo} alt="ProAxion Logo" className="proaxion-logo" />
      </header>
      { !isSidebarOpen && (
        <button className="hamburger-button" onClick={toggleSidebar}>
          <FaBars />
        </button>
      )}
      <Sidebar 
         isOpen={isSidebarOpen} 
         onClose={toggleSidebar}
         onHomeClick={handleHomeClick}
         onMachineTypeConfigurationClick={handleMachineTypeConfigurationClick}
         onMachineHealthClick={handleMachineHealthClick}
         onEnhanceSensorInstallsClick={handleEnhanceSensorInstallsClick}
         onOptimizeMachineDataClick={handleOptimizeMachineDataClick}
         onContactUsClick={handleContactUsClick}
      />
      {currentScreen === 'welcome' && (
        <WelcomeScreen
          onHomeClick={handleHomeClick}
          onMachineTypeConfigurationClick={handleMachineTypeConfigurationClick}
          onMachineHealthClick={handleMachineHealthClick}
          onEnhanceSensorInstallsClick={handleEnhanceSensorInstallsClick}
          onOptimizeMachineDataClick={handleOptimizeMachineDataClick}
        />
      )}
      {currentScreen === 'machineTypeConfiguration' && (
        <MachineTypeConfiguration onHomeClick={handleHomeClick} />
      )}
      {currentScreen === 'machineHealth' && (
        <MachineHealth onHomeClick={handleHomeClick} />
      )}
      {currentScreen === 'enhanceSensorInstalls' && (
        <EnhanceSensorInstalls onHomeClick={handleHomeClick} />
      )}
      {currentScreen === 'optimizeMachineData' && (
        <OptimizeMachineData onHomeClick={handleHomeClick} />
      )}
      {currentScreen === 'contact' && <ContactUs onBackClick={handleHomeClick} />}
    </div>
  );
}

export default App;

