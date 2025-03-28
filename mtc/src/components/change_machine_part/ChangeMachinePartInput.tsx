import React, { useState } from 'react';
import './ChangeMachinePartInput.css'; // Import the CSS file

interface ChangeMachinePartInputProps {
  onSubmit: (formData: Record<string, string>) => void;
  onHomeClick: () => void; // Add onHomeClick prop
}

const questions = [
  { name: 'changingComponent', label: 'Are you changing a machine component (e.g., motor, pump, gearbox)?', type: 'select' },
  { name: 'sameSensor', label: 'If it’s a new component, are you using the same sensor?', type: 'select' },
  { name: 'componentPartNumber', label: 'What is the component and part number?', type: 'text' },
  { name: 'sensorID', label: 'What is the sensor ID? (Scan the QR code)', type: 'text' },
  { name: 'installNewSensor', label: 'Do you know how to install the new sensor?', type: 'select' },
  { name: 'picturesInstalledSensor', label: 'Can you provide pictures of the installed sensor, showing it is already installed?', type: 'select' },
  { name: 'newSensorID', label: 'If it is a new sensor, what is the new sensor ID?', type: 'text' },
  { name: 'picturesOfSensor', label: 'Do you have pictures of the installed sensor?', type: 'select' },
  { name: 'uploadInfoToUI', label: 'Do you know how to upload this information to the UI?', type: 'select' },
];

const ChangeMachinePartInput: React.FC<ChangeMachinePartInputProps> = ({ onSubmit, onHomeClick }) => {
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      onSubmit(formData); // Submit the form on the last question
    }
  };

  const handleBack = () => {
    if (currentQuestionIndex === 0) {
      onHomeClick(); // Call onHomeClick when on the first question
    } else {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  const currentQuestion = questions[currentQuestionIndex];

  return (
    <div className="change-machine-part-input">
      <form className="form-container">
        <div className="question-container"> {/* Wrap h2 and input in a container */}
          <h2>{currentQuestion.label}</h2> {/* Display question text */}
          {currentQuestion.type === 'select' ? (
            <select
              name={currentQuestion.name}
              value={formData[currentQuestion.name] || ''}
              onChange={handleChange}
            >
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          ) : (
            <input
              type="text"
              name={currentQuestion.name}
              value={formData[currentQuestion.name] || ''}
              onChange={handleChange}
            />
          )}
        </div>
      </form>
      <div className="button-container"> {/* Buttons at the bottom */}
        <button type="button" onClick={handleBack}>
          {currentQuestionIndex === 0 ? 'Home' : 'Back'}
        </button>
        <button type="button" onClick={handleNext}>
          {currentQuestionIndex === questions.length - 1 ? 'Submit' : 'Next'}
        </button>
      </div>
    </div>
  );
};

export default ChangeMachinePartInput;
