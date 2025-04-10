// BeltDrivenFanMonitoring.tsx
import React, { useState, useEffect } from 'react';
import './BeltDrivenFanMonitoring.css';
import diagramDefault from '../assets/diagram_default.jpg';
import diagramFan from '../assets/diagram_fan.jpg';
import diagramBelt from '../assets/diagram_belt.jpg';
import diagramMotor from '../assets/diagram_motor.jpg';

interface Sensor {
  id: string;
  sensorId: string;
  position: string;
  direction: string;
  isAlert?: boolean;
}

interface BeltDrivenFanMonitoringProps {
  sensors: Sensor[];
  selectedSensorId: string | null;
}

const BeltDrivenFanMonitoring: React.FC<BeltDrivenFanMonitoringProps> = ({ sensors, selectedSensorId }) => {
  const [currentImage, setCurrentImage] = useState(diagramDefault);

  useEffect(() => {
    if (selectedSensorId) {
      switch (selectedSensorId) {
        case '558580230':
          setCurrentImage(diagramBelt);
          break;
        case '2':
          setCurrentImage(diagramFan);
          break;
        case '3':
          setCurrentImage(diagramMotor);
          break;
        default:
          setCurrentImage(diagramDefault);
      }
    } else {
      setCurrentImage(diagramDefault);
    }
  }, [selectedSensorId]);

  return (
    <div className="belt-driven-fan-monitoring">
      <div className="monitoring-content">
        <div className="machine-diagram">
          <img src={currentImage} alt="Machine Diagram" />
        </div>
      </div>
    </div>
  );
};

export default BeltDrivenFanMonitoring; 