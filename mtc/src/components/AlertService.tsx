// AlertService.tsx
// A mock service to check if a sensor is in alert state

export interface AlertInfo {
  sensorId: string;
  isAlert: boolean;
  alertMessage?: string;
}

// This simulates an API call to check sensor status
export const checkSensorAlerts = (sensorIds: string[]): Promise<AlertInfo[]> => {
  // Simulate a network delay
  return new Promise((resolve) => {
    setTimeout(() => {
      // Create results - in this mock, only sensor with ID "2" is in alert state
      const results = sensorIds.map(id => ({
        sensorId: id,
        isAlert: id === "2",
        alertMessage: id === "2" ? "High temperature detected" : undefined
      }));
      
      resolve(results);
    }, 800); // Simulate a delay of 800ms
  });
};