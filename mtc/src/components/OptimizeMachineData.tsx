import React from 'react';

interface OptimizeMachineDataProps {
  onHomeClick: () => void;
}

const OptimizeMachineData: React.FC<OptimizeMachineDataProps> = ({ onHomeClick }) => {
  return (
    <div className="optimize-machine-data">
      <h1>Optimize Machine Data</h1>
      <p>Coming Soon</p>
      <button onClick={onHomeClick}>Home</button>
    </div>
  );
};

export default OptimizeMachineData;