// MachineHealth.tsx
import React, { useState } from 'react';
import './MachineHealth.css';
import MachineHealthLeft from './MachineHealthLeft';
import MachineHealthRight from './MachineHealthRight';
import BeltDrivenFanMonitoring from './BeltDrivenFanMonitoring';
import { checkSensorAlerts } from './AlertService';

interface Sensor {
  id: string;
  sensorId: string;
  position: string;
  direction: string;
  isAlert?: boolean;
}

const MachineHealth: React.FC = () => {
  const [sensors, setSensors] = useState<Sensor[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [visibleSensorId, setVisibleSensorId] = useState<number | null>(null);

  const checkForAlerts = async () => {
    const sensorsWithIds = sensors.filter(sensor => sensor.sensorId.trim() !== '');
    if (sensorsWithIds.length === 0) return;

    setIsLoading(true);
    try {
      const sensorIds = sensorsWithIds.map(sensor => sensor.sensorId);
      const alertResults = await checkSensorAlerts(sensorIds);

      const updatedSensors = sensors.map(sensor => {
        const alertInfo = alertResults.find(alert => alert.sensorId === sensor.sensorId);
        return {
          ...sensor,
          isAlert: alertInfo ? alertInfo.isAlert : false
        };
      });
      setSensors(updatedSensors);
    } catch (error) {
      console.error('Error checking alerts:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mh-container">
      <div className="mh-left-panel">
        <h2>Sensor Marking & Input</h2>
        <MachineHealthLeft 
          sensors={sensors} 
          setSensors={setSensors} 
          onSubmit={checkForAlerts} 
          isLoading={isLoading}
          setVisibleSensorId={setVisibleSensorId}
        />
      </div>
      <div className="mh-right-panel">
        <h2>Sensor Diagnostics</h2>
        <BeltDrivenFanMonitoring 
          sensors={sensors}
          selectedSensorId={visibleSensorId?.toString()}
        />
        <MachineHealthRight 
          visibleSensorId={visibleSensorId}
        />
      </div>
    </div>
  );
};

export default MachineHealth;