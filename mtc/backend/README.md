# Machine Health Monitoring System 

## Overview
This is a backend service for a machine health monitoring system, primarily used for processing sensor data, image recognition, and status monitoring.

## Features
1. Sensor ID Detection
2. Image Processing and Analysis
3. Real-time Status Monitoring
4. Alert System

## Installation Steps

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

> Make sure to place your YOLOv8 model weights in `backend/model/weights/best.pt`.

---

### Frontend Setup

```bash
cd mtc
npm install
npm run dev
```

Access the app at: `http://localhost:5173`

---


##  Features

###  Frontend (React + TypeScript)

- Split view layout with left-side sensor input and right-side visual diagnostics
- **Manual or image-based sensor entry**
- Dynamic sensor preview with ID/location/status
- Component-specific warnings (bearing wear, misalignment, etc.)
- Machine type selection page (currently supports "Fan")

###  Backend (Flask + YOLOv8 + EasyOCR)

- `/api/detect-sensors` API accepts image uploads
- Uses **YOLOv8** to detect sensor areas
- Uses **EasyOCR** to extract numeric sensor IDs
- Returns bounding boxes + confidence + extracted IDs

---

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

