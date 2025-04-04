import React, { useState, useEffect } from 'react';
import './MTCInstructions.css';
import MTCInstructionSteps from './MTCInstructionSteps';
import instructionsData from '../data/instructions.json';

interface InstructionContent {
  subtitle?: string;
  text: string[];
}

interface InstructionPage {
  title: string;
  content: InstructionContent[];
}

const MTCInstructions: React.FC = () => {
  const [instructions, setInstructions] = useState<any[]>([]);
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
      {instructions.length > 0 && (
        <>
          {/* Pass currentPage as pageIndex */}
          <MTCInstructionSteps instruction={instructions[currentPage]} pageIndex={currentPage} />
          <div className="instructions-navigation">
            {currentPage > 0 ? (
              <button onClick={handleBack} className="nav-button back">
                Previous Step
              </button>
            ) : (
              // Render an empty placeholder so spacing stays consistent
              <div className="nav-button-placeholder" />
            )}
            <div className="see-video-button-container">
              {currentPage >= 3 && currentPage <= 7 && (
                <button 
                  className="nav-button video"
                  onClick={() => {
                    if (currentPage === 3) {
                      window.open("https://youtu.be/t2r8st6eWiM?si=wRbScKp5cZwLqC1i&t=3", "_blank");
                    } else if (currentPage === 4) {
                      window.open("https://youtu.be/t2r8st6eWiM?si=5qfMCCApgeiv34Js&t=39", "_blank");
                    } else if (currentPage === 5) {
                      window.open("https://youtu.be/t2r8st6eWiM?si=5qfMCCApgeiv34Js&t=66", "_blank");
                    } else if (currentPage === 6) {
                      window.open("https://youtu.be/t2r8st6eWiM?si=BkF3zjolGGukubgY&t=48", "_blank");
                    } else if (currentPage === 7) {
                      window.open("https://youtu.be/t2r8st6eWiM?si=5qfMCCApgeiv34Js&t=77", "_blank");
                    }
                  }}
                >
                  See Video
                </button>
              )}
            </div>
            {currentPage < totalPages - 1 ? (
              <button onClick={handleNext} className="nav-button next">
                Next Step
              </button>
            ) : (
              // Render an empty placeholder if needed
              <div className="nav-button-placeholder" />
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default MTCInstructions;