import React, { createContext, useState, ReactNode } from 'react';

interface MachineContextType {
  machineType: string;
  transmissionType: string;
  currentInstallationStep: number;
  setMachineType: (type: string) => void;
  setTransmissionType: (type: string) => void;
  setCurrentInstallationStep: (step: number) => void;
}

const defaultContext: MachineContextType = {
  machineType: 'Fan',
  transmissionType: 'Belt-Driven',
  currentInstallationStep: 0,
  setMachineType: () => {},
  setTransmissionType: () => {},
  setCurrentInstallationStep: () => {},
};

export const MachineContext = createContext<MachineContextType>(defaultContext);

interface MachineContextProviderProps {
  children: ReactNode;
}

export const MachineContextProvider: React.FC<MachineContextProviderProps> = ({ children }) => {
  const [machineType, setMachineType] = useState<string>('Fan');
  const [transmissionType, setTransmissionType] = useState<string>('Belt-Driven');
  const [currentInstallationStep, setCurrentInstallationStep] = useState<number>(0);

  return (
    <MachineContext.Provider
      value={{
        machineType,
        transmissionType,
        currentInstallationStep,
        setMachineType,
        setTransmissionType,
        setCurrentInstallationStep,
      }}
    >
      {children}
    </MachineContext.Provider>
  );
};