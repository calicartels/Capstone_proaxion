import "./Sidebar.css";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onHomeClick: () => void;
  onMachineTypeConfigurationClick: () => void;
  onMachineHealthClick: () => void;
  onContactUsClick: () => void;
  onEnhanceSensorInstallsClick: () => void;
  onOptimizeMachineDataClick: () => void;
}

export function Sidebar({ isOpen, onClose, onHomeClick, onMachineTypeConfigurationClick, onMachineHealthClick, onContactUsClick, onEnhanceSensorInstallsClick, onOptimizeMachineDataClick }: SidebarProps) {
  return (
    <div className={`sidebar ${isOpen ? "sidebar-open" : ""}`}>
      <button className="close-button" onClick={onClose}>Close</button>
      <ul>
        <li onClick={onHomeClick}>Home</li>
        <li onClick={onMachineTypeConfigurationClick}>Install New Sensors</li>
        <li onClick={onEnhanceSensorInstallsClick}>Enhance Sensor Installs</li>
        <li onClick={onMachineHealthClick}>Trouble Shoot Machine</li>
        <li onClick={onOptimizeMachineDataClick}>Optimize Machine Data</li>
        <li onClick={onContactUsClick}>Contact Us</li>
      </ul>
    </div>
  );
}