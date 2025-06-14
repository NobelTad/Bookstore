from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS
from pos import generate_poster  # your poster generator

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

    pdf_file = request.files['file']
    if pdf_file.filename == '' or not pdf_file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid PDF file'}), 400

    try:
        data = json.loads(request.form['json'])
    except Exception as e:
        return jsonify({'error': f'Invalid JSON data: {str(e)}'}), 400

    # Only require name and description
    required_fields = ['name', 'description']
    missing_or_empty = [field for field in required_fields if field not in data or not data[field]]
    if missing_or_empty:
        return jsonify({'error': f'Missing or empty fields in JSON: {missing_or_empty}'}), 400

    # Remove 'url' if present (optional but clean)
    data.pop('url', None)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    pdf_filename = f"{timestamp}.pdf"
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    pdf_file.save(pdf_path)

    # 👇 Save poster to uploads/poster/
    poster_folder = os.path.join(UPLOAD_FOLDER, 'poster')
    os.makedirs(poster_folder, exist_ok=True)
    poster_filename = f"{timestamp}.jpg"
    poster_path = os.path.join(poster_folder, poster_filename)
    generate_poster(pdf_path, poster_path)

    # 👇 Save JSON with poster info
    json_filename = f"{timestamp}.json"
    json_path = os.path.join(DATA_FOLDER, json_filename)
    data['poster_name'] = os.path.join('poster', poster_filename)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({
        'message': f'PDF and JSON saved successfully: {pdf_filename} and {json_filename}',
        'pdf_file': pdf_filename,
        'json_file': json_filename,
        'poster_name': os.path.join('poster', poster_filename)
    }), 200


@app.route('/download/<path:filepath>', methods=['GET'])
def download_file(filepath):
    safe_path = secure_filename(os.path.basename(filepath))
    full_path = os.path.join(UPLOAD_FOLDER, filepath)

    if not os.path.isfile(full_path):
        return jsonify({'error': 'File not found'}), 404

    return send_from_directory(UPLOAD_FOLDER, filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
