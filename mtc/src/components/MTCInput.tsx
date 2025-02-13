import './MTCInput.css';

interface MTCInputProps {
  onBackClick: () => void;
}

function MTCInput({ onBackClick }: MTCInputProps) {
  return (
    <div>
      <h2>Type of Machine</h2>
      <select>
        <option value="MT1">Fan</option>
        <option value="MT2">Other</option>
      </select>
      
      <div className="button-container">
        <button onClick={onBackClick}>Back</button>
        <button>Next</button>
      </div>
    </div>
  );
}

export default MTCInput;