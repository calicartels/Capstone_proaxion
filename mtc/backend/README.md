# Machine Health Monitoring System Backend

## Overview
This is a backend service for a machine health monitoring system, primarily used for processing sensor data, image recognition, and status monitoring.

## Features
1. Sensor ID Detection
2. Image Processing and Analysis
3. Real-time Status Monitoring
4. Alert System

## Installation Steps

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Model Files
Place the trained YOLO model file `best.pt` in:
```
mtc/backend/model/weights/best.pt
```

## Start Service
```bash
python app.py
```
Service will start at http://localhost:5000

## API Endpoints

### 1. Sensor Detection
- Endpoint: `/api/detect-sensors`
- Method: POST
- Parameters: 
  - image: Image file

### 2. Status Query
- Endpoint: `/api/sensor-status`
- Method: GET
- Parameters: 
  - sensor_id: Sensor ID

## Machine Health Features

### 1. Sensor Management
- Support both manual input and image upload for adding sensors

### 2. Status Monitoring
- Normal
- Warning
- Alert

### 3. Machine Information
- Belt-driven fan specifications
- Installation location
- Maintenance records

### 4. Fault Diagnosis
System can help users identify machine health issues

## Troubleshooting
1. If OCR recognition fails, ensure image clarity is sufficient
2. If service fails to start, check if port 5000 is occupied

## Future Extensions
The system supports future database integration for storing sensor historical data, maintenance records, and other information to facilitate data analysis and long-term monitoring.
