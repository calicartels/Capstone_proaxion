import React, { useState } from 'react';
import { FaBars } from 'react-icons/fa';
import WelcomeScreen from './components/WelcomeScreen';
import MachineTypeConfiguration from './components/MachineTypeConfiguration';
import MachineHealth from './components/MachineHealth';
import EnhanceSensorInstalls from './components/EnhanceSensorInstalls';
import OptimizeMachineData from './components/OptimizeMachineData';
import CreateMaintenancePlan from './components/create_maintenance_plan/CreateMaintenancePlan';
import ContactUs from './components/ContactUs';
import { Sidebar } from './components/Sidebar';
import MachineSelection from './components/MachineSelection'; // 💡 新增导入
import './App.css';
import ProAxionLogo from './assets/ProAxion-logo.png';

function App() {
  const [currentScreen, setCurrentScreen] = useState('welcome');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [selectedMachineType, setSelectedMachineType] = useState<string | null>(null);

  const handleHomeClick = () => {
    setCurrentScreen('welcome');
    setIsSidebarOpen(false);
    setSelectedMachineType(null); 
  };

  const handleMachineTypeConfigurationClick = () => {
    setCurrentScreen('machineTypeConfiguration');
    setIsSidebarOpen(false);
  };

  const handleMachineHealthClick = () => {
    setCurrentScreen('machineSelection'); 
    setIsSidebarOpen(false);
  };

  const handleMachineSelected = (machineType: string) => {
    setSelectedMachineType(machineType);
    setCurrentScreen('machineHealth');
  };

  const handleEnhanceSensorInstallsClick = () => {
    setCurrentScreen('enhanceSensorInstalls');
    setIsSidebarOpen(false);
  };

  const handleOptimizeMachineDataClick = () => {
    setCurrentScreen('optimizeMachineData');
    setIsSidebarOpen(false);
  };

  const handleCreateMaintenancePlanClick = () => {
    setCurrentScreen('createMaintenancePlan');
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
      {!isSidebarOpen && (
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

      {/*website */}
      {currentScreen === 'welcome' && (
        <WelcomeScreen
          onHomeClick={handleHomeClick}
          onMachineTypeConfigurationClick={handleMachineTypeConfigurationClick}
          onMachineHealthClick={handleMachineHealthClick}
          onEnhanceSensorInstallsClick={handleEnhanceSensorInstallsClick}
          onOptimizeMachineDataClick={handleOptimizeMachineDataClick}
          onCreateMaintenancePlanClick={handleCreateMaintenancePlanClick}
        />
      )}

      {currentScreen === 'machineSelection' && (
        <MachineSelection 
          onMachineSelected={handleMachineSelected} 
          onHomeClick={handleHomeClick}
        />
      )}

      {currentScreen === 'machineHealth' && selectedMachineType === 'fan' && (
        <MachineHealth onHomeClick={handleHomeClick} />
      )}

      {currentScreen === 'machineTypeConfiguration' && (
        <MachineTypeConfiguration onHomeClick={handleHomeClick} />
      )}

      {currentScreen === 'enhanceSensorInstalls' && (
        <EnhanceSensorInstalls onHomeClick={handleHomeClick} />
      )}

      {currentScreen === 'optimizeMachineData' && (
        <OptimizeMachineData onHomeClick={handleHomeClick} />
      )}

      {currentScreen === 'createMaintenancePlan' && (
        <CreateMaintenancePlan onHomeClick={handleHomeClick} />
      )}

      {currentScreen === 'contact' && <ContactUs onBackClick={handleHomeClick} />}
    </div>
  );
}

export default App;
