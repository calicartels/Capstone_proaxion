import "./Sidebar.css";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onHomeClick: () => void;
  onMachineTypeConfigurationClick: () => void;
  onMachineHealthClick: () => void;
}

export function Sidebar({ isOpen, onClose, onHomeClick, onMachineTypeConfigurationClick, onMachineHealthClick }: SidebarProps) {  return (
    <div className={`sidebar ${isOpen ? "sidebar-open" : ""}`}>
      <button onClick={onClose}>Close</button>
      <ul>
        <li onClick={onHomeClick}>Home</li>
        <li onClick={onMachineTypeConfigurationClick}>Install New Sensors</li>
        <li>Enhance Sensor Installs</li>
        <li onClick={onMachineHealthClick}>Trouble Shoot Machine</li>
        <li>Optimize Machine Data</li>
        <li>Contact Us</li>
      </ul>
    </div>
  );
}