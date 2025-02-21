import React from 'react';

interface EnhanceSensorInstallsProps {
  onHomeClick: () => void;
}

const EnhanceSensorInstalls: React.FC<EnhanceSensorInstallsProps> = ({ onHomeClick }) => {
  return (
    <div className="enhance-sensor-installs">
      <h1>Enhance Sensor Installs</h1>
      <p>Coming Soon</p>
      <button onClick={onHomeClick}>Home</button>
    </div>
  );
};

export default EnhanceSensorInstalls;