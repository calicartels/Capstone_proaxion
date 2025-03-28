import React from 'react';
import ChangeMachinePartInput from './ChangeMachinePartInput'; // Import ChangeMachinePartInput

interface ChangeMachinePartProps {
  onHomeClick: () => void;
}

const ChangeMachinePart: React.FC<ChangeMachinePartProps> = ({ onHomeClick }) => {
  const handleFormSubmit = (formData: Record<string, string>) => {
    console.log('Form Data Submitted:', formData);
    // Handle form submission logic here
  };

  return (
    <div className="change-machine-part">
      <h1>Change a Machine Part</h1>
      <ChangeMachinePartInput onSubmit={handleFormSubmit} onHomeClick={onHomeClick} /> {/* Pass onHomeClick */}
    </div>
  );
};

export default ChangeMachinePart;