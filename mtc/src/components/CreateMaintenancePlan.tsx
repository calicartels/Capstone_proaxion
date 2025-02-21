import React from 'react';

interface CreateMaintenancePlanProps {
  onHomeClick: () => void;
}

const CreateMaintenancePlan: React.FC<CreateMaintenancePlanProps> = ({ onHomeClick }) => {
  return (
    <div className="create-maintenance-plan">
      <h1>Create a Maintenance Plan</h1>
      {/* Add additional content as needed */}
      <button onClick={onHomeClick}>Home</button>
    </div>
  );
};

export default CreateMaintenancePlan;