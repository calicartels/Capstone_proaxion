// BeltDrivenFanMonitoring.js
import React, { useState } from 'react';
import './BeltDrivenFanMonitoring.css'; // Make sure to create this CSS file

const BeltDrivenFanMonitoring = () => {
  // Define sensor data with locations, statuses, and descriptions
  const [sensors, setSensors] = useState([
    {
      id: 1,
      name: 'Fan Bearing Sensor',
      x: 110,
      y: 170,
      status: 'alert', // alert, warning, normal
      vibration: '12.5 mm/s',
      lastReading: '10 min ago',
      message: 'High vibration detected. Possible bearing wear or misalignment.',
      possibleIssues: [
        'Bearing damage or wear',
        'Fan wheel imbalance',
        'Shaft misalignment',
        'Loose mounting bolts'
      ]
    },
    {
      id: 2,
      name: 'Motor Bearing Sensor',
      x: 325,
      y: 170,
      status: 'normal',
      vibration: '2.1 mm/s',
      lastReading: '5 min ago',
      message: 'Normal operation detected.',
      possibleIssues: []
    },
    {
      id: 3, 
      name: 'Belt Tension Sensor',
      x: 210,
      y: 145,
      status: 'warning',
      vibration: '5.7 mm/s',
      lastReading: '8 min ago',
      message: 'Elevated vibration levels. Verify belt tension and condition.',
      possibleIssues: [
        'Belt tension too high or too low',
        'Belt wear or damage',
        'Pulley misalignment',
        'Belt slippage'
      ]
    }
  ]);

  const [selectedSensor, setSelectedSensor] = useState(null);

  // Handler for clicking on a sensor
  const handleSensorClick = (sensor) => {
    setSelectedSensor(sensor);
  };

  // Get color based on sensor status
  const getSensorColor = (status) => {
    switch (status) {
      case 'alert': return 'red';
      case 'warning': return 'orange';
      case 'normal': return 'green';
      default: return 'gray';
    }
  };

  // Get CSS class for status badge
  const getStatusClass = (status) => {
    switch (status) {
      case 'alert': return 'status-badge alert';
      case 'warning': return 'status-badge warning';
      case 'normal': return 'status-badge normal';
      default: return 'status-badge';
    }
  };

  return (
    <div className="container">
      <h1 className="title">Belt Driven Fan Monitoring</h1>
      <div className="panel">
        {/* Main visualization container */}
        <div className="visualization">
          {/* Fan */}
          <div className="fan">
            <div className="fan-inner">
              <div className="fan-hub">
                <div className="fan-center"></div>
              </div>
            </div>
          </div>
          
          {/* Fan housing */}
          <div className="fan-housing"></div>
          
          {/* Motor */}
          <div className="motor">
            <div className="motor-detail top"></div>
            <div className="motor-detail middle"></div>
            <div className="motor-detail bottom"></div>
          </div>
          
          {/* Motor shaft */}
          <div className="motor-shaft"></div>
          
          {/* Fan shaft */}
          <div className="fan-shaft"></div>
          
          {/* Belt */}
          <div className="belt-circle left"></div>
          <div className="belt-circle right"></div>
          <div className="belt-straight top"></div>
          <div className="belt-straight bottom"></div>
          
          {/* Sensors */}
          {sensors.map(sensor => (
            <div 
              key={sensor.id}
              className="sensor"
              style={{
                top: `${sensor.y}px`,
                left: `${sensor.x}px`,
                backgroundColor: getSensorColor(sensor.status),
              }}
              onClick={() => handleSensorClick(sensor)}
            >
              <div className="sensor-label">{sensor.id}</div>
            </div>
          ))}
        </div>
        
        {/* Legend */}
        <div className="legend">
          <div className="legend-item">
            <div className="legend-color normal"></div>
            <span>Normal</span>
          </div>
          <div className="legend-item">
            <div className="legend-color warning"></div>
            <span>Warning</span>
          </div>
          <div className="legend-item">
            <div className="legend-color alert"></div>
            <span>Alert</span>
          </div>
        </div>
        
        {/* Sensor details panel */}
        {selectedSensor ? (
          <div className="details-panel">
            <div className="details-header">
              <h3 className="details-title">{selectedSensor.name}</h3>
              <span className={getStatusClass(selectedSensor.status)}>
                {selectedSensor.status.toUpperCase()}
              </span>
            </div>
            
            <div className="details-grid">
              <div className="details-item">
                <span className="details-label">Vibration Level:</span> {selectedSensor.vibration}
              </div>
              <div className="details-item">
                <span className="details-label">Last Reading:</span> {selectedSensor.lastReading}
              </div>
            </div>
            
            <p className="details-message">{selectedSensor.message}</p>
            
            {selectedSensor.possibleIssues.length > 0 && (
              <div className="issues-container">
                <h4 className="issues-title">Possible Issues:</h4>
                <ul className="issues-list">
                  {selectedSensor.possibleIssues.map((issue, index) => (
                    <li key={index} className="issue-item">{issue}</li>
                  ))}
                </ul>
              </div>
            )}
            
            <button 
              className="close-button"
              onClick={() => setSelectedSensor(null)}
            >
              Close
            </button>
          </div>
        ) : (
          <div className="details-panel empty">
            Click on a sensor to view details and troubleshooting information
          </div>
        )}
      </div>

      <div className="panel machine-info">
        <h2 className="section-title">Machine Information</h2>
        <div className="info-grid">
          <div className="info-column">
            <h3 className="info-title">Belt-Driven Fan</h3>
            <ul className="info-list">
              <li>Fan Sheave Diameter: 12 inches</li>
              <li>Motor Sheave Diameter: 4 inches</li>
              <li>Center-to-Center Distance: 24 inches</li>
              <li>Belt Type: V-Belt (A-Section)</li>
            </ul>
          </div>
          <div className="info-column">
            <h3 className="info-title">Operating Parameters</h3>
            <ul className="info-list">
              <li>Fan Speed: 800 RPM</li>
              <li>Motor Speed: 1750 RPM</li>
              <li>Typical Vibration Range: 0.5-3.0 mm/s</li>
              <li>Last Maintenance: 45 days ago</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BeltDrivenFanMonitoring;