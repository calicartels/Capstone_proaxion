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
  onChange?: React.ChangeEventHandler<HTMLSelectElement>;
}

export default function MTCInput({ title, options, value, onChange }: MTCInputProps) {
  return (
    <div className="mtc-input-container">
      <h2>{title}</h2>
      <select 
          value={value} 
          onChange={onChange} 
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
}