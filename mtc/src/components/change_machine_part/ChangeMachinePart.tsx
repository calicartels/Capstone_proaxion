import React from 'react';

interface ChangeMachinePartProps {
  onHomeClick: () => void;
}

const ChangeMachinePart: React.FC<ChangeMachinePartProps> = ({ onHomeClick }) => {
  const handleFormSubmit = (formData: Record<string, string>) => {
    console.log('Form Data Submitted:', formData);
    // Handle form submission logic here
  };

  return (
    <div className="change-sensor">
      <h1>Change a Machine Part</h1>

      
    </div>
  );
};

export default ChangeSensor;