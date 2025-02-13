import './MTCInput.css';

interface MTCInputProps {
  onBackClick: () => void;
  onNextClick: () => void;
  title: string;
  options: { value: string; label: string }[];
}

function MTCInput({ onBackClick, onNextClick, title, options }: MTCInputProps) {
  return (
    <div>
      <h2>{title}</h2>
      <select>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      
      <div className="button-container">
        <button onClick={onBackClick}>Back</button>
        <button onClick={onNextClick}>Next</button>
      </div>
    </div>
  );
}

export default MTCInput;