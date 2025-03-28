import React, { useState } from 'react';
import './MachineHealth.css';
import MachineHealthLeft from './MachineHealthLeft';
import MachineHealthRight from './MachineHealthRight';
import { checkSensorAlerts, AlertInfo } from './AlertService';

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
  isAlert?: boolean; // Flag to indicate if this sensor is in alert state
}

const MachineHealth: React.FC = () => {
  // Shared state for sensors
  const [sensors, setSensors] = useState<Sensor[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  // Function to check for alerts and update sensor status
  const checkForAlerts = async () => {
    // Only proceed if there are sensors with IDs
    const sensorsWithIds = sensors.filter(sensor => sensor.sensorId.trim() !== '');
    if (sensorsWithIds.length === 0) {
      alert('Please add sensors and set their IDs before submitting');
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Get sensor IDs for alert check
      const sensorIds = sensorsWithIds.map(sensor => sensor.sensorId);
      
      // Call the mock alert service
      const alertResults = await checkSensorAlerts(sensorIds);
      
      // Update sensors with alert information
      const updatedSensors = sensors.map(sensor => {
        const alertInfo = alertResults.find(alert => alert.sensorId === sensor.sensorId);
        return {
          ...sensor,
          isAlert: alertInfo ? alertInfo.isAlert : false
        };
      });
      
      // Update the state with new sensor information
      setSensors(updatedSensors);
      
      // Show alert message if any sensors are in alert state
      const alertingSensors = alertResults.filter(result => result.isAlert);
      if (alertingSensors.length > 0) {
        alert(`Alert! ${alertingSensors.length} sensor(s) reporting issues.`);
      } else {
        alert('All sensors are normal.');
      }
    } catch (error) {
      console.error('Error checking alerts:', error);
      alert('Error occurred while checking sensor status');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mh-container">
      {/* Left Panel: Sensor Marking & Input Area (60% width) */}
      <div className="mh-left-panel">
        <h2>Sensor Marking & Input</h2>
        <MachineHealthLeft 
          sensors={sensors} 
          setSensors={setSensors} 
          onSubmit={checkForAlerts}
          isLoading={isLoading}
        />
      </div>
      
      {/* Right Panel: Chatbot Interaction Area (40% width) */}
      <div className="mh-right-panel">
        <h2>Diagnostic Assistant</h2>
        <MachineHealthRight 
          sensors={sensors}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
};

export default MachineHealth;