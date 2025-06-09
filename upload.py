from flask import Flask, request, jsonify,send_from_directory
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files or 'json' not in request.form:
        return jsonify({'error': 'Missing file or JSON data'}), 400

    # Validate PDF file first
    pdf_file = request.files['file']
    if pdf_file.filename == '' or not pdf_file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid PDF file'}), 400

    # Parse and validate JSON data
    try:
        data = json.loads(request.form['json'])
    except Exception as e:
        return jsonify({'error': f'Invalid JSON data: {str(e)}'}), 400

    # Check required keys and non-empty values
    required_fields = ['name', 'description', 'url']
    missing_or_empty = [field for field in required_fields if field not in data or not data[field]]
    if missing_or_empty:
        return jsonify({'error': f'Missing or empty fields in JSON: {missing_or_empty}'}), 400

    # All good, save files with timestamped names
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    pdf_filename = f"{timestamp}.pdf"
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    pdf_file.save(pdf_path)

    json_filename = f"{timestamp}.json"
    json_path = os.path.join(DATA_FOLDER, json_filename)
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({
        'message': f'PDF and JSON saved successfully: {pdf_filename} and {json_filename}',
        'pdf_file': pdf_filename,
        'json_file': json_filename
    }), 200

#the fileserving mechanizm
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    safe_name = secure_filename(filename)
    return send_from_directory(UPLOAD_FOLDER, safe_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
