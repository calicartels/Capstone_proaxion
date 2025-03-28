import React, { useState, useRef, useEffect } from 'react';
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

interface ChatMessage {
  sender: 'system';
  text: string;
}

interface MachineHealthRightProps {
  sensors: Sensor[];
  isLoading: boolean;
}

const MachineHealthRight: React.FC<MachineHealthRightProps> = ({ 
  sensors, 
  isLoading
}) => {
  // State for chat messages
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    { sender: 'system', text: 'Hello! I am your machine health assistant. I can help you diagnose issues with your sensors.' }
  ]);
  
  // Reference for auto-scrolling
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Auto-scroll to latest message
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages]);
  
  // Effect to detect when sensors change or when alerts are detected
  useEffect(() => {
    const alertSensors = sensors.filter(sensor => sensor.isAlert);
    
    if (alertSensors.length > 0 && !isLoading) {
      // Generate diagnostic messages for each alert sensor
      alertSensors.forEach(sensor => {
        const diagnosisMessage = generateDiagnosisMessage(sensor);
        
        setTimeout(() => {
          setChatMessages(prev => [
            ...prev,
            { 
              sender: 'system', 
              text: `⚠️ Alert detected for sensor ${sensor.id} (${sensor.sensorId})!\n\n${diagnosisMessage}` 
            }
          ]);
        }, 500);
      });
    } else if (sensors.length > 0 && !isLoading) {
      // If sensors are submitted but no alerts
      const completeSensors = sensors.filter(s => s.sensorId && s.position && s.direction);
      if (completeSensors.length > 0) {
        setTimeout(() => {
          setChatMessages(prev => [
            ...prev,
            { 
              sender: 'system', 
              text: `✅ All sensors are normal. No issues detected with the ${completeSensors.length} sensor(s) you've submitted.` 
            }
          ]);
        }, 500);
      }
    }
  // Only trigger when isLoading changes from true to false (submission completed)
  // or when the alert status of sensors changes
  }, [isLoading, sensors.map(s => s.isAlert).join(',')]);
  
  // Generate diagnosis message based on sensor position and direction
  const generateDiagnosisMessage = (sensor: Sensor): string => {
    const { position, direction } = sensor;
    
    // Return appropriate diagnostic message based on position and direction
    if (position === 'Motor DE' && direction === 'Horizontal') {
      return "You might want to take a look around the drive shaft and coupling. It could be worth checking if the alignment seems a bit off there.";
    } else if (position === 'Motor DE' && direction === 'Vertical') {
      return "Perhaps consider checking the motor base and how it's mounted. A quick glance at the vertical setup might reveal if everything is stable.";
    } else if (position === 'Motor NDE' && direction === 'Horizontal') {
      return "It might be a good idea to inspect the motor housing and mounting bolts on the non-drive side. Sometimes a casual check can show if things aren't sitting quite right horizontally.";
    } else if (position === 'Motor NDE' && direction === 'Vertical') {
      return "You could also check the support structure and base alignment at the non-drive end. A brief look at the vertical mounting might help spot any issues.";
    } else if (position === 'Bearing DE' && direction === 'Horizontal') {
      return "Maybe take a moment to check the drive-end bearing's alignment in the horizontal plane. It's always good to ensure things are lined up properly there.";
    } else if (position === 'Bearing DE' && direction === 'Vertical') {
      return "Consider having a look at the vertical mounting of the drive-end bearing. A simple check might reveal if the support looks as it should.";
    } else if (position === 'Bearing NDE' && direction === 'Horizontal') {
      return "It might be worthwhile to inspect the horizontal installation of the non-drive-end bearing. Sometimes even a slight misalignment can be a clue.";
    } else if (position === 'Bearing NDE' && direction === 'Vertical') {
      return "Perhaps take a quick look at the vertical support and mounting of the non-drive-end bearing. A casual check might help you rule out any obvious issues.";
    } else {
      return "I recommend checking this sensor's installation and surrounding components for any obvious issues.";
    }
  };

  return (
    <div className="mh-chatbot-container">
      <div className="mh-chat-messages">
        {chatMessages.map((msg, index) => (
          <div 
            key={index} 
            className="mh-system-message"
          >
            <div className="mh-message-content">
              {msg.text.split('\n').map((line, i) => (
                <p key={i}>{line}</p>
              ))}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default MachineHealthRight;
