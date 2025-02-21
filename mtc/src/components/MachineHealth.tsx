import React from 'react';

interface MachineHealthProps {
  onHomeClick: () => void;
}

function MachineHealth({ onHomeClick }: MachineHealthProps) {
  return (
    <div>
      <h1>Trouble Shoot a Machine</h1>
      <button onClick={onHomeClick}>Home</button>
    </div>
  );
}

export default MachineHealth;