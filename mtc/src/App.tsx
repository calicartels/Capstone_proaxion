import React, { useState } from 'react';
import { FaBars } from 'react-icons/fa';
import WelcomeScreen from './components/WelcomeScreen';
import MachineTypeConfiguration from './components/MachineTypeConfiguration';
import MachineHealth from './components/MachineHealth';
import ContactUs from './components/ContactUs';
import { Sidebar } from './components/Sidebar';
import './App.css';

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

  const handleContactUsClick = () => {
    setCurrentScreen('contact');
    setIsSidebarOpen(false);
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="App">
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
         onContactUsClick={handleContactUsClick}
      />
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

