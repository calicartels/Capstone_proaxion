import { useState } from "react"
import "./App.css"
import WelcomeScreen from "./components/WelcomeScreen.tsx"
import { HamburgerMenu } from "./components/HamburgerMenu.tsx"
import ProAxionLogo from "./assets/ProAxion-logo.png"

function App() {
  return (
    <>
      <WelcomeScreen />
      <HamburgerMenu />
      <footer className="app-footer">
        <img src={ ProAxionLogo } alt="Proaxion Logo" className="proaxion-logo" />
      </footer>
    </>
  )
}

export default App

