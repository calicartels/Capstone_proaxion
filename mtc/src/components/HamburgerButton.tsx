import './HamburgerButton.css';

interface HamburgerButtonProps {
  onClick: () => void;
}

export function HamburgerButton({ onClick }: HamburgerButtonProps) {
  return (
    <button onClick={onClick} className="hamburger-button">
      &#9776; {/* Unicode character for hamburger icon */}
    </button>
  );
}