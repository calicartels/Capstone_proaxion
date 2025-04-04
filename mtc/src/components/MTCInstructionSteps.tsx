import React from 'react';
import './MTCInstructionSteps.css';

interface InstructionContent {
  subtitle?: string;
  text: string[];
}

interface InstructionPage {
  title: string;
  content: InstructionContent[];
}

interface MTCInstructionStepsProps {
  instruction: InstructionPage;
  pageIndex: number;
}

const MTCInstructionSteps: React.FC<MTCInstructionStepsProps> = ({ instruction, pageIndex }) => {
  return (
    <div className="mtc-instructions">
      <h2>{instruction.title}</h2>
      {pageIndex >= 2 && pageIndex <= 8 && (
        <div className="instruction-step-image-container">
          <img 
            src={`/assets/dat_step${pageIndex - 1}.png`} 
            alt={`Step ${pageIndex} illustration`} 
            className="instruction-step-image" 
          />
        </div>
      )}
      <div className="instructions-content">
        {instruction.content.map((section, index) => (
          <div key={index}>
            {section.subtitle && <h3>{section.subtitle}</h3>}
            {section.text && section.text.map((paragraph, idx) => (
              <p key={idx}>{paragraph}</p>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MTCInstructionSteps;