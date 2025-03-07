import React from 'react';
import './MTCInput.css';

interface Option {
  value: string;
  label: string;
}

interface MTCInputProps {
  title: string;
  options: Option[];
  value?: string;
  onChange?: (value: string) => void;
}

const MTCInput: React.FC<MTCInputProps> = ({ title, options, value, onChange }) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (onChange) {
      onChange(e.target.value);
    }
  };

  return (
    <div className="mtc-input-container">
      <h2>{title}</h2>
      <select 
        value={value || options[0]?.value} 
        onChange={handleChange} 
        className="mtc-input-dropdown"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default MTCInput;