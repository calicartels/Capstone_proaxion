import MTCInput from './MTCInput.tsx';
import './MachineTypeConfiguration.css';

interface MachineTypeConfigurationProps {
  onHomeClick: () => void;
}

function MachineTypeConfiguration({ onHomeClick }: MachineTypeConfigurationProps) {
  return (
    <div className="machine-type-configuration-container">
      <h1>Machine Type Configuration</h1>
      <div className="machine-type-configuration">
        <MTCInput onBackClick={onHomeClick} />
      </div>
    </div>
  );
}

export default MachineTypeConfiguration;