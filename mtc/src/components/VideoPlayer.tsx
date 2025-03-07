import React, { useRef, useEffect, useContext, useState } from 'react';
import { MachineContext } from '../context/MachineContext';
import './VideoPlayer.css';

// Installation steps mapping with timestamps (in seconds)
export const installationSteps = [
  {
    id: 'materials',
    name: 'Materials Required',
    timeRange: [5, 7],
    promptTriggers: ['materials', 'get started', 'what do i need'],
    instruction: "First, let's gather the materials needed for installation."
  },
  {
    id: 'markSpot',
    name: 'Mark the Spot',
    timeRange: [9, 38],
    promptTriggers: ['mark', 'spot', 'location', 'next step'],
    instruction: 'Use an indent tool or drill a small pilot hole to mark the exact location for the sensor.'
  },
  {
    id: 'tapHole',
    name: 'Tap the Hole',
    timeRange: [38, 46],
    promptTriggers: ['tap', 'thread', 'create threads'],
    instruction: 'Use a ¼"-28 thread tap to create the screw threads in the hole.'
  },
  {
    id: 'threadLocker',
    name: 'Apply Thread Locker',
    timeRange: [50, 65],
    promptTriggers: ['thread locker', 'blue', 'vibra-tite'],
    instruction: "Apply a semi-permanent thread locker to the sensor's stud threads."
  },
  {
    id: 'silicone',
    name: 'Apply Silicone Sealant',
    timeRange: [65, 81],
    promptTriggers: ['silicone', 'sealant', 'prevent corrosion'],
    instruction: 'Apply silicone sealant to the flat surface created by the spot-face tool to prevent corrosion.'
  },
  {
    id: 'installation',
    name: 'Install Sensor',
    timeRange: [84, 101],
    promptTriggers: ['install', 'screw', 'hand-tighten'],
    instruction: 'Screw the sensor into the tapped hole by hand. Do not use any tools.'
  }
];

const VideoPlayer: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const { currentInstallationStep } = useContext(MachineContext);
  const [currentStep, setCurrentStep] = useState<number>(-1);
  
  // Video source - using your provided path
  const videoSrc = 'chatbot_rag/video/sensor_installation_drill_tap.mp4';

  // Handle clicks on step indicators
  const handleStepClick = (index: number) => {
    setCurrentStep(index);
    if (videoRef.current && index >= 0 && index < installationSteps.length) {
      const [startTime] = installationSteps[index].timeRange;
      videoRef.current.currentTime = startTime;
      videoRef.current.play();
    }
  };

  // Update video when the installation step changes (from chatbot)
  useEffect(() => {
    if (currentInstallationStep !== currentStep) {
      setCurrentStep(currentInstallationStep);
    }
  }, [currentInstallationStep]);

  // Update video when step changes
  useEffect(() => {
    if (!videoRef.current) return;
    
    if (currentStep >= 0 && currentStep < installationSteps.length) {
      const step = installationSteps[currentStep];
      const [startTime] = step.timeRange;
      
      // Set video time to start of current step
      videoRef.current.currentTime = startTime;
      videoRef.current.play().catch(err => {
        console.error("Error playing video:", err);
      });
    }
  }, [currentStep]);

  return (
    <div className="video-player-container">
      <h2>Installation Instructions</h2>
      <div className="video-wrapper">
        <video 
          ref={videoRef}
          className="installation-video"
          controls
          src={videoSrc}
        >
          Your browser does not support the video tag.
        </video>
      </div>
      <div className="step-indicators">
        {installationSteps.map((step, index) => (
          <div 
            key={step.id}
            className={`step-indicator ${index === currentStep ? 'active' : ''}`}
            onClick={() => handleStepClick(index)}
          >
            {step.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default VideoPlayer;