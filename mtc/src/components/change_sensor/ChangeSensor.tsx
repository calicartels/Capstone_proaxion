import React from 'react';
import ChangeSensorInputs from './ChangeSensorInputs';

interface ChangeSensorProps {
  onHomeClick: () => void;
}

const ChangeSensor: React.FC<ChangeSensorProps> = ({ onHomeClick }) => {
  const handleFormSubmit = (formData: Record<string, string>) => {
    console.log('Form Data Submitted:', formData);
    // Handle form submission logic here
  };

  return (
    <div className="change-sensor">
      <h1>Change a Sensor</h1>
      <ChangeSensorInputs onSubmit={handleFormSubmit} />
      
    </div>
  );
};

export default ChangeSensor;