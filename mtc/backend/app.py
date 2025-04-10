from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
import cv2
import easyocr
import re
import uuid
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Upload folder config
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load YOLO model and EasyOCR
try:
    logger.info("Loading YOLO model...")
    model = YOLO('model/weights/best.pt')
    logger.info("YOLO model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load YOLO model: {str(e)}")
    raise

try:
    logger.info("Initializing EasyOCR...")
    reader = easyocr.Reader(['en'], gpu=False)
    logger.info("EasyOCR initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize EasyOCR: {str(e)}")
    raise

def process_image(image_path):
    """Process image and return detection results"""
    try:
        # Read image
        logger.info(f"Reading image: {image_path}")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Failed to read image")

        # YOLO detection
        logger.info("Running YOLO detection...")
        results = model(image)[0]
        logger.info(f"Detection completed. Found {len(results.boxes)} objects")

        # Process detections
        detected_ids = []
        for i, box in enumerate(results.boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cropped = image[y1:y2, x1:x2]

            # OCR
            logger.info(f"Running OCR on object {i + 1}")
            ocr_result = reader.readtext(cropped)
            if ocr_result:
                text = ocr_result[0][1]
                digits = re.findall(r'\d+', text)
                if digits:
                    full_id = ''.join(digits)
                    logger.info(f"Detected ID: {full_id}")
                    detected_ids.append({
                        'id': full_id,
                        'confidence': float(box.conf[0]),
                        'position': {
                            'x1': int(x1),
                            'y1': int(y1),
                            'x2': int(x2),
                            'y2': int(y2)
                        }
                    })

        return detected_ids

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise

@app.route('/api/detect-sensors', methods=['POST'])
def detect_sensors():
    """Handle sensor detection request"""
    logger.info("Received image upload request")

    if 'image' not in request.files:
        logger.error("No image file in request")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        logger.error("Empty filename")
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        logger.error(f"Invalid file type: {file.filename}")
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(f"{timestamp}_{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save uploaded file
        logger.info(f"Saving file to: {filepath}")
        file.save(filepath)

        # Process image
        detected_ids = process_image(filepath)

        # Clean up uploaded file
        logger.info("Removing uploaded file")
        os.remove(filepath)

        return jsonify({
            'success': True,
            'detected_sensors': detected_ids,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error in detect_sensors: {str(e)}")
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
