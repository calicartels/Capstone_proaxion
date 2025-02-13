import { useState } from "react"
import "./App.css"
import WelcomeScreen from "./components/WelcomeScreen.tsx"
import { HamburgerMenu } from "./components/HamburgerMenu.tsx"
import MachineTypeConfiguration from "./components/MachineTypeConfiguration.tsx"
import MachineHealth from "./components/MachineHealth.tsx"
import ProAxionLogo from "./assets/ProAxion-logo.png"

function App() {
  const [showWelcomeScreen, setShowWelcomeScreen] = useState(true);
  const [showMachineTypeConfiguration, setShowMachineTypeConfiguration] = useState(false);
  const [showMachineHealth, setShowMachineHealth] = useState(false);

  const handleHomeClick = () => {
    setShowWelcomeScreen(true);
    setShowMachineTypeConfiguration(false);
    setShowMachineHealth(false);
  };
  const handleMachineTypeConfigurationClick = () => {
    setShowWelcomeScreen(false);
    setShowMachineTypeConfiguration(true);
    setShowMachineHealth(false);
  };
  const handleMachineHealthClick = () => {
    setShowWelcomeScreen(false);
    setShowMachineTypeConfiguration(false);
    setShowMachineHealth(true);
  };

  return (
    <>
      { showWelcomeScreen && (
        <WelcomeScreen 
          onHomeClick={handleHomeClick}
          onMachineTypeConfigurationClick={handleMachineTypeConfigurationClick} 
          onMachineHealthClick={handleMachineHealthClick}
        /> 
      )}
      { showMachineTypeConfiguration && (
        <MachineTypeConfiguration 
          onHomeClick={handleHomeClick} 
        /> 
      )}
      { showMachineHealth && <MachineHealth /> }

      <HamburgerMenu 
        onHomeClick={handleHomeClick}
        onMachineTypeConfigurationClick={handleMachineTypeConfigurationClick}
        onMachineHealthClick={handleMachineHealthClick}
      />
      
      <footer className="app-footer">
        <img src={ ProAxionLogo } alt="Proaxion Logo" className="proaxion-logo" />
      </footer>
    </>
  )
}

export default App

