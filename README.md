# Capstone Project - ProAxion

## Project Overview
ProAxion's Capstone Project is a web-based application designed to assist users in monitoring and maintaining industrial machines. The application provides step-by-step instructions for configuring machines, changing sensors, and creating maintenance plans.

## Features
- **Machine Configuration**: Guide users through the process of configuring new machines.
- **Sensor Replacement**: Step-by-step instructions for replacing sensors.
- **Maintenance Planning**: Tools to create and manage maintenance plans.
- **Interactive Chatbot**: Provides real-time assistance during configuration and maintenance tasks.
- **Dynamic Instructions**: Instructions adapt based on user inputs.

## Install Instructions
1. Download and install [Node.js](https://nodejs.org/).
2. Open a terminal and navigate to the `mtc` folder:
   ```bash
   cd mtc
   ```
3. Install dependencies:
   ```bash
   npm install
   ```

## Launch Instructions
1. Open a terminal and navigate to the `mtc` folder:
   ```bash
   cd mtc
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. Open your browser and navigate to the URL provided in the terminal output (e.g., `http://localhost:3000`).

## Folder Structure
```
Capstone_proaxion/
├── mtc/
│   ├── public/                # Static assets (e.g., images, icons)
│   │   ├── assets/            # Images and other static files
│   │   ├── index.html         # Main HTML file
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── change_sensor/ # Components for sensor replacement
│   │   │   │   ├── ChangeSensor.tsx
│   │   │   │   ├── ChangeSensorInputs.tsx
│   │   │   │   ├── ChangeSensorInputs.css
│   │   │   ├── create_maintenance_plan/ # Components for maintenance planning
│   │   │   │   ├── CreateMaintenancePlan.tsx
│   │   │   ├── shared/        # Shared components used across features
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   ├── ...            # Other feature-specific components
│   │   ├── data/              # JSON files for instructions and other data
│   │   │   ├── instructions.json
│   │   ├── styles/            # Global CSS styles
│   │   │   ├── variables.css  # CSS variables for consistent styling
│   │   │   ├── global.css     # Global styles applied across the app
│   │   ├── App.tsx            # Main application component
│   │   ├── main.tsx           # Application entry point
│   ├── package.json           # Project dependencies and scripts
│   ├── tsconfig.json          # TypeScript configuration
│   ├── vite.config.ts         # Vite configuration
│   ├── ...                    # Other configuration files
```

## How to Contribute
We welcome contributions to improve this project! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push your changes to your fork:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request to the main repository.

## Technologies Used
- **Frontend**: React, TypeScript, CSS
- **Build Tool**: Vite
- **Package Manager**: npm

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact the project team at [support@proaxion.com](mailto:support@proaxion.com).