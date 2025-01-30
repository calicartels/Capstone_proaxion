import "./Sidebar.css";

export function Sidebar({ isOpen, onClose }: { isOpen: boolean, onClose: () => void }) {
  return (
    <div className={`sidebar ${isOpen ? "sidebar-open" : ""}`}>
      <button onClick={onClose}>Close</button>
      <ul>
        <li>Machine Type Configuration</li>
        <li>Machine Health</li>
      </ul>
    </div>
  );
}