import React, { useState } from 'react';
import './MachineSelection.css';

interface MachineSelectionProps {
  onMachineSelected: (machineType: string) => void;
  onHomeClick: () => void;
}

function MachineSelection({ onMachineSelected, onHomeClick }: MachineSelectionProps) {
  const [selectedMachine, setSelectedMachine] = useState<string>('');

  const handleMachineChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedMachine(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedMachine) {
      onMachineSelected(selectedMachine);
    }
  };

  return (
    <div className="machine-selection-container">
      <h2 className="section-title">Machine Selection</h2>
      <div className="panel">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="machineType">Select Machine Type:</label>
            <select 
              id="machineType"
              value={selectedMachine} 
              onChange={handleMachineChange}
              className="form-control"
              required
            >
              <option value="">-- Select a machine --</option>
              <option value="fan">Fan</option>
            </select>
          </div>
          <button 
            type="submit" 
            className="submit-button"
            disabled={!selectedMachine}
          >
            Next
          </button>
        </form>
      </div>
    </div>
  );
}

export default MachineSelection; 