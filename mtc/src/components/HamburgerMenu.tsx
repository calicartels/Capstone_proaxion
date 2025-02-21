import * as React from "react";
import { Sidebar } from "./Sidebar";
import { HamburgerButton } from "./HamburgerButton";

interface HamburgerMenuProps {
  onHomeClick: () => void;
  onMachineTypeConfigurationClick: () => void;
  onMachineHealthClick: () => void;
  onContactUsClick: () => void; // Add this line
}

function HamburgerMenu({ onHomeClick, onMachineTypeConfigurationClick, onMachineHealthClick, onContactUsClick }: HamburgerMenuProps) {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState<boolean>(false);

  const openSidebar = () => {
    console.log("Opening sidebar");
    setIsSidebarOpen(true);
  };

  const closeSidebar = () => {
    console.log("Closing sidebar");
    setIsSidebarOpen(false);
  };

  return (
    <div>
      {!isSidebarOpen && <HamburgerButton onClick={openSidebar} />}
      <Sidebar 
        isOpen={isSidebarOpen} 
        onClose={closeSidebar} 
        onHomeClick={onHomeClick}
        onMachineTypeConfigurationClick={onMachineTypeConfigurationClick}
        onMachineHealthClick={onMachineHealthClick}
        onContactUsClick={onContactUsClick} // Pass the prop
      />
    </div>
  );
}

export { HamburgerMenu };