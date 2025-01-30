import './WelcomeScreen.css';

export default function WelcomeScreen() {
  return (
      <div className="welcome-screen">
        <h1>Machine Assistant</h1>
        <div className="button-container">
          <button>Machine Type Configuration</button>
          <button>Machine Health</button>
        </div>
      </div>
  );
}