import React, { useState, useRef } from 'react';
import './MachineHealth.css';

interface SensorRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

interface Sensor {
  id: string;
  rect: SensorRect;
  sensorId: string;
  position: string;
  direction: string;
  notes: string;
  isAlert?: boolean;
}

interface MachineHealthLeftProps {
  sensors: Sensor[];
  setSensors: React.Dispatch<React.SetStateAction<Sensor[]>>;
  onSubmit: () => Promise<void>;
  isLoading: boolean;
}

const MachineHealthLeft: React.FC<MachineHealthLeftProps> = ({ 
  sensors, 
  setSensors, 
  onSubmit,
  isLoading
}) => {
  // State management
  const [image, setImage] = useState<string | null>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [startPoint, setStartPoint] = useState({ x: 0, y: 0 });
  const [currentRect, setCurrentRect] = useState<SensorRect | null>(null);
  
  // References
  const imageContainerRef = useRef<HTMLDivElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  
  // Image upload handler
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setImage(event.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };
  
  // Rectangle drawing functions
  const handleMouseDown = (e: React.MouseEvent) => {
    if (!image) return;
    
    const container = imageContainerRef.current;
    if (!container) return;
    
    const rect = container.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    setIsDrawing(true);
    setStartPoint({ x, y });
    setCurrentRect({ x, y, width: 0, height: 0 });
  };
  
  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDrawing || !image) return;
    
    const container = imageContainerRef.current;
    if (!container) return;
    
    const rect = container.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const width = x - startPoint.x;
    const height = y - startPoint.y;
    
    setCurrentRect({
      x: width > 0 ? startPoint.x : x,
      y: height > 0 ? startPoint.y : y,
      width: Math.abs(width),
      height: Math.abs(height)
    });
  };
  
  const handleMouseUp = () => {
    if (!isDrawing || !currentRect || !image) return;
    
    // Only add the sensor if the rectangle is big enough
    if (currentRect.width > 10 && currentRect.height > 10) {
      // Create a new sensor with the next sequential ID
      const nextSensorNumber = sensors.length + 1;
      const newSensor: Sensor = {
        id: `sensor${nextSensorNumber}`,
        rect: { ...currentRect },
        sensorId: '', // Empty string for user to input
        position: '',
        direction: '',
        notes: '',
        isAlert: false
      };
      
      setSensors([...sensors, newSensor]);
    }
    
    setIsDrawing(false);
    setCurrentRect(null);
  };
  
  // Update sensor information
  const updateSensorInfo = (index: number, field: keyof Sensor, value: string) => {
    const updatedSensors = [...sensors];
    updatedSensors[index] = {
      ...updatedSensors[index],
      [field]: value
    };
    setSensors(updatedSensors);
  };
  
  // Delete sensor and renumber remaining sensors
  const deleteSensor = (index: number) => {
    // First, remove the sensor at the specified index
    const filteredSensors = sensors.filter((_, i) => i !== index);
    
    // Then, renumber all the remaining sensors
    const renumberedSensors = filteredSensors.map((sensor, i) => ({
      ...sensor,
      id: `sensor${i + 1}`
    }));
    
    // Update state with the renumbered sensors
    setSensors(renumberedSensors);
  };
  
  // Submit all sensor data
  const submitSensorData = async () => {
    // Check if all required fields are filled
    const incompleteFields = sensors.filter(sensor => 
      !sensor.sensorId || !sensor.position || !sensor.direction
    );
    
    if (incompleteFields.length > 0) {
      alert(`Please complete all required fields for ${incompleteFields.length} sensor(s)`);
      return;
    }
    
    // Trigger the onSubmit handler (which will check for alerts)
    await onSubmit();
  };

  return (
    <div className="mh-left-content">
      <div className="mh-upload-section">
        <h3>Upload Machine Image</h3>
        <input 
          type="file" 
          accept="image/*" 
          onChange={handleImageUpload} 
          className="mh-file-input"
        />
      </div>
      
      <div 
        className="mh-image-container" 
        ref={imageContainerRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        {image ? (
          <div className="mh-relative-container">
            <img 
              src={image} 
              alt="Machine" 
              className="mh-device-image" 
              ref={imageRef}
            />
            
            {/* Rectangle being drawn */}
            {isDrawing && currentRect && (
              <div 
                className="mh-sensor-rect mh-drawing"
                style={{
                  left: `${currentRect.x}px`,
                  top: `${currentRect.y}px`,
                  width: `${currentRect.width}px`,
                  height: `${currentRect.height}px`
                }}
              ></div>
            )}
            
            {/* Saved sensor rectangles */}
            {sensors.map((sensor, index) => (
              <div 
                key={sensor.id}
                className={`mh-sensor-rect ${sensor.isAlert ? 'mh-sensor-alert' : ''}`}
                style={{
                  left: `${sensor.rect.x}px`,
                  top: `${sensor.rect.y}px`,
                  width: `${sensor.rect.width}px`,
                  height: `${sensor.rect.height}px`
                }}
              >
                <span className={`mh-sensor-label ${sensor.isAlert ? 'mh-label-alert' : ''}`}>
                  {sensor.id}
                  {sensor.isAlert && ' ⚠️'}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div className="mh-upload-placeholder">
            Please upload a machine image to start marking sensors
          </div>
        )}
      </div>
      
      {/* Sensor information input area */}
      <div className="mh-sensor-info-section">
        <h3>Sensor Information</h3>
        {sensors.length === 0 ? (
          <p>Mark sensors on the image by drawing rectangles</p>
        ) : (
          <>
            <div className="mh-sensor-forms">
              {sensors.map((sensor, index) => (
                <div 
                  key={sensor.id} 
                  className={`mh-sensor-form ${sensor.isAlert ? 'mh-form-alert' : ''}`}
                >
                  <h4>
                    {sensor.id}
                    {sensor.isAlert && (
                      <span className="mh-alert-indicator"> ALERT!</span>
                    )}
                  </h4>
                  <div className="mh-form-group">
                    <label>Sensor ID</label>
                    <input 
                      type="text"
                      value={sensor.sensorId}
                      onChange={(e) => updateSensorInfo(index, 'sensorId', e.target.value)}
                      placeholder="Enter sensor ID"
                      className={sensor.isAlert ? 'mh-input-alert' : ''}
                    />
                  </div>
                  
                  <div className="mh-form-group">
                    <label>Component/Position</label>
                    <select
                      value={sensor.position}
                      onChange={(e) => updateSensorInfo(index, 'position', e.target.value)}
                      className={sensor.isAlert ? 'mh-input-alert' : ''}
                    >
                      <option value="">Select position</option>
                      <option value="Motor DE">Motor DE</option>
                      <option value="Motor NDE">Motor NDE</option>
                      <option value="Bearing DE">Bearing DE</option>
                      <option value="Bearing NDE">Bearing NDE</option>
                    </select>
                  </div>
                  
                  <div className="mh-form-group">
                    <label>Direction/Axis</label>
                    <select
                      value={sensor.direction}
                      onChange={(e) => updateSensorInfo(index, 'direction', e.target.value)}
                      className={sensor.isAlert ? 'mh-input-alert' : ''}
                    >
                      <option value="">Select direction</option>
                      <option value="Vertical">Vertical</option>
                      <option value="Horizontal">Horizontal</option>
                    </select>
                  </div>
                  
                  <div className="mh-form-group">
                    <label>Notes</label>
                    <textarea
                      value={sensor.notes}
                      onChange={(e) => updateSensorInfo(index, 'notes', e.target.value)}
                      placeholder="Optional: Add installation background, maintenance records, etc."
                      className={sensor.isAlert ? 'mh-input-alert' : ''}
                    ></textarea>
                  </div>
                  
                  <button 
                    className="mh-delete-btn"
                    onClick={() => deleteSensor(index)}
                  >
                    Delete Sensor
                  </button>
                </div>
              ))}
            </div>
            
            <button 
              className="mh-submit-btn"
              onClick={submitSensorData}
              disabled={isLoading}
            >
              {isLoading ? 'Checking Sensors...' : 'Submit Sensor Data'}
            </button>
            
            {isLoading && (
              <div className="mh-loading">
                <div className="mh-loading-spinner"></div>
                <span>Processing...</span>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default MachineHealthLeft;