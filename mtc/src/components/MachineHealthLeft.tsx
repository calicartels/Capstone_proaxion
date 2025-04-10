// MachineHealthLeft.tsx
import React, { useState, useRef } from 'react';
import './MachineHealth.css';

interface Sensor {
  id: string;
  sensorId: string;
  position: string;
  direction: string;
  isAlert?: boolean;
}

interface MachineHealthLeftProps {
  sensors: Sensor[];
  setSensors: React.Dispatch<React.SetStateAction<Sensor[]>>;
  onSubmit: () => Promise<void>;
  isLoading: boolean;
  setVisibleSensorId: (id: number) => void;
}

const MachineHealthLeft: React.FC<MachineHealthLeftProps> = ({ 
  sensors, setSensors, onSubmit, isLoading, setVisibleSensorId 
}) => {
  const [inputMethod, setInputMethod] = useState<'manual' | 'image'>('manual');
  const [sensorId, setSensorId] = useState('');
  const [position, setPosition] = useState('');
  const [direction, setDirection] = useState('');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  // Store last submitted sensor ID
  const lastSubmittedId = useRef('');

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (inputMethod === 'manual') {
      if (!sensorId || !position || !direction) return;
      const parsedId = parseInt(sensorId);
      setVisibleSensorId(parsedId);
      lastSubmittedId.current = sensorId;

      const newSensor: Sensor = {
        id: `sensor${sensors.length + 1}`,
        sensorId,
        position,
        direction,
        isAlert: false
      };

      setSensors(prev => [...prev, newSensor]);
    } else {
      if (!selectedImage) return;
      
      const newSensor: Sensor = {
        id: `sensor${sensors.length + 1}`,
        sensorId: '558580230',
        position: 'Auto Detected',
        direction: 'Auto Detected',
        isAlert: false
      };
      
      setSensors(prev => [...prev, newSensor]);
      setVisibleSensorId(558580230);
    }

    await onSubmit();
  };

  // Clear inputs only when a new ID is entered and submitted again
  React.useEffect(() => {
    if (isLoading === false && lastSubmittedId.current !== '' && sensorId !== lastSubmittedId.current) {
      setSensorId('');
      setPosition('');
      setDirection('');
      lastSubmittedId.current = '';
    }
  }, [sensorId, isLoading]);

  return (
    <div className="mh-left-content">
      <div className="mh-sensor-form-container">
        <h3>Sensor Information</h3>
        <div className="mh-input-method-selector">
          <label>Input Method:</label>
          <select 
            value={inputMethod} 
            onChange={(e) => setInputMethod(e.target.value as 'manual' | 'image')}
          >
            <option value="manual">Manual Input</option>
            <option value="image">Upload Image</option>
          </select>
        </div>

        <form className="mh-manual-form" onSubmit={handleSubmit}>
          {inputMethod === 'manual' ? (
            <>
              <div className="mh-form-group">
                <label>Sensor ID (Numeric)</label>
                <input 
                  type="number"
                  value={sensorId}
                  onChange={(e) => setSensorId(e.target.value)}
                  placeholder="Enter sensor ID"
                  required
                />
              </div>

              <div className="mh-form-group">
                <label>Component/Position</label>
                <select
                  value={position}
                  onChange={(e) => setPosition(e.target.value)}
                  required
                >
                  <option value="">Select position</option>
                  <option value="Fan Bearing Sensor">Fan Bearing Sensor</option>
                  <option value="Belt Tension Sensor">Belt Tension Sensor</option>
                  <option value="Motor Bearing Sensor">Motor Bearing Sensor</option>
                </select>
              </div>

              <div className="mh-form-group">
                <label>Direction/Axis</label>
                <select
                  value={direction}
                  onChange={(e) => setDirection(e.target.value)}
                  required
                >
                  <option value="">Select direction</option>
                  <option value="Horizontal">Horizontal</option>
                  <option value="Vertical">Vertical</option>
                </select>
              </div>
            </>
          ) : (
            <div className="mh-form-group">
              <label>Upload Image</label>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                required
              />
              {imagePreview && (
                <div className="mh-image-preview">
                  <img src={imagePreview} alt="Preview" />
                </div>
              )}
            </div>
          )}

          <button type="submit" className="mh-submit-btn" disabled={isLoading}>
            {isLoading ? 'Processing...' : 'Submit Sensor Data'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default MachineHealthLeft;
