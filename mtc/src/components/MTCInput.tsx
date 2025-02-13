import React from 'react';
import './MTCInput.css';

interface MTCInputProps {
  title: string;
  options: { value: string; label: string }[];
}

const MTCInput: React.FC<MTCInputProps> = ({ title, options }) => {
  return (
    <div className="mtc-input-container">
      <h2>{title}</h2>
      <select>
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