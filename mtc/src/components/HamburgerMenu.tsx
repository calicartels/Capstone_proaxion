"use client"

import * as React from "react";
import { Sidebar } from "./Sidebar";
import { HamburgerButton } from "./HamburgerButton";

export function HamburgerMenu() {
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
      <Sidebar isOpen={isSidebarOpen} onClose={closeSidebar} />
    </div>
  );
}