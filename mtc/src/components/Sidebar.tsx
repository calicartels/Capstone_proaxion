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
  onCreateMaintenancePlan: () => void;
  onChangeSensorClick: () => void;
  onChangeMachineComponentClick: () => void;
}

export function Sidebar({
  isOpen,
  onClose,
  onHomeClick,
  onMachineTypeConfigurationClick,
  onMachineHealthClick,
  onContactUsClick,
  onEnhanceSensorInstallsClick,
  onOptimizeMachineDataClick,
  onCreateMaintenancePlan,
  onChangeSensorClick,
  onChangeMachineComponentClick
}: SidebarProps) {
  return (
    <div className={`sidebar ${isOpen ? "sidebar-open" : ""}`}>
      <button className="close-button" onClick={onClose}>Close</button>
      <ul>
        <li onClick={onHomeClick}>Home</li>
        <li onClick={onMachineTypeConfigurationClick}>Monitor a New Machine</li>
        <li onClick={onMachineHealthClick}>Trouble Shoot a Machine</li>
        <li onClick={onEnhanceSensorInstallsClick}>Update an Existing Machine</li>
        <li onClick={onOptimizeMachineDataClick}>Add Machine Data</li>
        <li onClick={onChangeSensorClick}>Change a Sensor</li>
        <li onClick={onChangeMachineComponentClick}>Change a Machine Component</li>
        <li onClick={onCreateMaintenancePlan}>Create a Maintenance Plan</li>
        <li onClick={onContactUsClick}>Contact Us</li>
      </ul>
    </div>
  );
}