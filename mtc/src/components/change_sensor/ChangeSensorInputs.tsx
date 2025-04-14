import React, { useState } from 'react';
import './ChangeSensorInputs.css';

interface ChangeSensorInputsProps {
  onSubmit: (formData: Record<string, string>) => void;
}

const ChangeSensorInputs: React.FC<ChangeSensorInputsProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    previousSensorId: '',
    knowsInstallation: '',
    knowsUploadInfo: '',
    newSensorId: '',
    hasPictures: '',
    knowsUploadToUI: '',
  });

  const [currentQuestion, setCurrentQuestion] = useState(0);

  const questions = [
    {
      label: 'What is the ID of the previous sensor?',
      input: (
        <input
          type="text"
          name="previousSensorId"
          value={formData.previousSensorId}
          onChange={(e) => handleChange(e)}
        />
      ),
    },
    {
      label: 'Do you know how to install the new sensor?',
      input: (
        <select
          name="knowsInstallation"
          value={formData.knowsInstallation}
          onChange={(e) => handleChange(e)}
        >
          <option value="">Select</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      ),
    },
    {
      label: 'Do you know how to upload the new sensor and component information?',
      input: (
        <select
          name="knowsUploadInfo"
          value={formData.knowsUploadInfo}
          onChange={(e) => handleChange(e)}
        >
          <option value="">Select</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      ),
    },
    {
      label: 'What is the new sensor ID?',
      input: (
        <input
          type="text"
          name="newSensorId"
          value={formData.newSensorId}
          onChange={(e) => handleChange(e)}
        />
      ),
    },
    {
      label: 'Do you have pictures of the installed sensor?',
      input: (
        <select
          name="hasPictures"
          value={formData.hasPictures}
          onChange={(e) => handleChange(e)}
        >
          <option value="">Select</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      ),
    },
    {
      label: 'Do you know how to upload the sensor information to the UI?',
      input: (
        <select
          name="knowsUploadToUI"
          value={formData.knowsUploadToUI}
          onChange={(e) => handleChange(e)}
        >
          <option value="">Select</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      ),
    },
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
    }
  };

  const handleBack = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion((prev) => prev - 1);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (currentQuestion === questions.length - 1) {
      onSubmit(formData);
    }
  };

  return (
    <form className="change-sensor-inputs" onSubmit={handleSubmit}>
      <div>
        <h2>{questions[currentQuestion].label}</h2>
        {questions[currentQuestion].input}
      </div>
      <div className="navigation-buttons">
        <button
          type="button"
          onClick={currentQuestion === 0 ? () => window.location.reload() : handleBack}
        >
          {currentQuestion === 0 ? 'Home' : 'Back'}
        </button>
        {currentQuestion < questions.length - 1 ? (
          <button type="button" onClick={handleNext}>
            Next
          </button>
        ) : (
          <button type="submit">Submit</button>
        )}
      </div>
    </form>
  );
};

export default ChangeSensorInputs;
