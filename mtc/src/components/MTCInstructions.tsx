import React, { useState, useEffect } from 'react';
import './MTCInstructions.css';
import MTCInstructionSteps from './MTCInstructionSteps';
import instructionsData from '../data/instructions.json';

interface InstructionPage {
  title: string;
  content: string[];
}

const MTCInstructions: React.FC = () => {
  const [instructions, setInstructions] = useState<InstructionPage[]>([]);
  const [currentPage, setCurrentPage] = useState(0);

  useEffect(() => {
    setInstructions(instructionsData);
  }, []);

  const totalPages = instructions.length;

  const handleNext = () => {
    if (currentPage < totalPages - 1) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handleBack = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div className="instructions-container">
      <MTCInstructionSteps instruction={instructions[currentPage]} />
      <div className="instructions-navigation">
        {currentPage > 0 && (
          <button onClick={handleBack} className="nav-button back">Back</button>
        )}
        {currentPage < totalPages - 1 && (
          <button onClick={handleNext} className="nav-button next">Next</button>
        )}
      </div>
    </div>
  );
};

export default MTCInstructions;