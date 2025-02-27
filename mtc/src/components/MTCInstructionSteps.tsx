import React, { useState, useEffect } from 'react';
import './MTCInstructionSteps.css';
import instructionsData from '../data/instructions.json';

interface InstructionPage {
  title: string;
  content: string[];
}

const MTCInstructionsSte: React.FC = () => {
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
    <div className="mtc-instructions">
      <h2>{instructions[currentPage]?.title}</h2>
      <div className="instructions-content">
        {instructions[currentPage]?.content.map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
    </div>
  );
};

const MTCInstructionSteps: React.FC<MTCInstructionStepsProps> = ({ instruction }) => {
  return (
    <div className="mtc-instructions">
      <h2>{instruction.title}</h2>
      <div className="instructions-content">
        {instruction.content.map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
    </div>
  );
};

export default MTCInstructionsSte;
export { MTCInstructionSteps };