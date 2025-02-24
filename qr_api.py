from flask import Flask, request, jsonify
import fitz  # PyMuPDF to read PDF
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
import os

app = Flask(__name__)

# ✅ Function to Extract QR Code from PDF
def extract_qr_code_from_pdf(pdf_path):
    """Extracts QR Code from a PDF file"""
    try:
        images = convert_from_path(pdf_path, dpi=300)

        for img in images:
            img_np = np.array(img)  # Convert PIL image to numpy array
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
            decoded_objects = decode(gray)  # Decode QR code
            
            for obj in decoded_objects:
                return obj.data.decode("utf-8")  # Return QR code text

        return None  # If no QR code is found
    except Exception as e:
        return str(e)

# ✅ Flask API Route
@app.route('/extract_qr', methods=['POST'])
def extract_qr():
    """API to process uploaded PDF and return QR data"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    pdf_path = "uploads/" + file.filename
    os.makedirs("uploads", exist_ok=True)  # Create upload directory if not exists
    file.save(pdf_path)

    qr_data = extract_qr_code_from_pdf(pdf_path)
    
    if qr_data:
        return jsonify({'qr_data': qr_data})
    else:
        return jsonify({'error': 'No QR Code found'}), 404

# ✅ Run Flask API
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
