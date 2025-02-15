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
        <li onClick={onMachineTypeConfigurationClick}>Machine Type Configuration</li>
        <li onClick={onMachineHealthClick}>Machine Health</li>
      </ul>
    </div>
  );
}