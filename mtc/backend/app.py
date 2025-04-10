from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
import cv2
import easyocr
import re
import uuid

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 加载模型和OCR
model = YOLO('model/weights/best.pt')
reader = easyocr.Reader(['en'], gpu=False)

@app.route('/api/detect-sensors', methods=['POST'])
def detect_sensors():
    print("Received image upload request")
    if 'image' not in request.files:
        print("No image file in request")
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['image']
    if file.filename == '':
        print("Empty filename")
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        print(f"Processing file: {file.filename}")
        # 生成唯一文件名
        filename = secure_filename(str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower())
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File saved to: {filepath}")
        
        try:
            # 读取图像
            image = cv2.imread(filepath)
            print("Image loaded successfully")
            
            # 使用YOLO进行检测
            print("Starting YOLO detection...")
            results = model(filepath)[0]
            print(f"YOLO detection completed. Found {len(results.boxes)} objects")
            
            # 处理检测结果
            detected_ids = []
            for i, box in enumerate(results.boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cropped = image[y1:y2, x1:x2]
                
                # OCR识别
                print(f"Processing OCR for object {i+1}")
                ocr_result = reader.readtext(cropped)
                if ocr_result:
                    text = ocr_result[0][1]
                    digits = re.findall(r'\d+', text)
                    if digits:
                        full_id = ''.join(digits)
                        print(f"Detected ID: {full_id}")
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
            
            # 清理上传的文件
            os.remove(filepath)
            print("Processing completed successfully")
            
            return jsonify({
                'success': True,
                'detected_sensors': detected_ids
            })
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            # 确保在出错时也清理文件
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': '不支持的文件类型'}), 400

if __name__ == '__main__':
    app.run(debug=True)
