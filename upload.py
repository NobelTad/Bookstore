from flask import Flask, request, jsonify, send_from_directory,abort
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS
from pos import generate_poster
from db import insert_book  # import here
from db import getrows
app = Flask(__name__)
CORS(app)
from db import getinfo
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

    required_fields = ['name', 'description']
    missing_or_empty = [field for field in required_fields if field not in data or not data[field]]
    if missing_or_empty:
        return jsonify({'error': f'Missing or empty fields in JSON: {missing_or_empty}'}), 400

    data.pop('url', None)  # Remove url if present

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    pdf_filename = f"{timestamp}.pdf"
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    pdf_file.save(pdf_path)

    poster_folder = os.path.join(UPLOAD_FOLDER, 'poster')
    os.makedirs(poster_folder, exist_ok=True)
    poster_filename = f"{timestamp}.jpg"
    poster_path = os.path.join(poster_folder, poster_filename)
    generate_poster(pdf_path, poster_path)

    # Use single slash URL paths only
    url_path = pdf_filename.replace('\\', '/')
    poster_path_rel = os.path.join('poster', poster_filename).replace('\\', '/')

    # Save JSON locally as well if needed
    json_filename = f"{timestamp}.json"
    json_path = os.path.join(DATA_FOLDER, json_filename)
    data['poster_name'] = poster_path_rel
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    # Call insert_book from db.py with all 4 fields
    book_id = insert_book(
        data['name'],
        data['description'],
        url_path,
        poster_path_rel
    )

    return jsonify({
        'message': f'PDF and JSON saved successfully with DB id {book_id}',
        'pdf_file': pdf_filename,
        'json_file': json_filename,
        'poster_name': poster_path_rel,
        'db_id': book_id
    }), 200
@app.route('/rows')
def rows():
    data = getrows()
    return jsonify(data)

@app.route('/fetch/<int:page>')
def fetch_page(page):
    per_page = 20

    # Call your getinfo() that returns JSON string of all rows
    all_data_json = getinfo()

    # Parse JSON string into Python list of dicts
    all_data = json.loads(all_data_json)

    start = (page - 1) * per_page
    end = start + per_page

    # Slice the data for current page
    page_data = all_data[start:end]

    return jsonify(page_data)
# your /download endpoint remains unchanged
@app.route('/files/<path:filename>')
def serve_file(filename):
    # Securely join the path to prevent directory traversal attacks
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Check if the file exists and is inside UPLOAD_FOLDER
    if os.path.isfile(full_path) and os.path.commonpath([os.path.abspath(full_path), os.path.abspath(UPLOAD_FOLDER)]) == os.path.abspath(UPLOAD_FOLDER):
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        abort(404)





from flask import Flask, request, jsonify, send_from_directory,abort
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS
from pos import generate_poster
from db import insert_book  # import here
from db import getrows
app = Flask(__name__)
CORS(app)
from db import getinfo
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

    required_fields = ['name', 'description']
    missing_or_empty = [field for field in required_fields if field not in data or not data[field]]
    if missing_or_empty:
        return jsonify({'error': f'Missing or empty fields in JSON: {missing_or_empty}'}), 400

    data.pop('url', None)  # Remove url if present

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    pdf_filename = f"{timestamp}.pdf"
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    pdf_file.save(pdf_path)

    poster_folder = os.path.join(UPLOAD_FOLDER, 'poster')
    os.makedirs(poster_folder, exist_ok=True)
    poster_filename = f"{timestamp}.jpg"
    poster_path = os.path.join(poster_folder, poster_filename)
    generate_poster(pdf_path, poster_path)

    # Use single slash URL paths only
    url_path = pdf_filename.replace('\\', '/')
    poster_path_rel = os.path.join('poster', poster_filename).replace('\\', '/')

    # Save JSON locally as well if needed
    json_filename = f"{timestamp}.json"
    json_path = os.path.join(DATA_FOLDER, json_filename)
    data['poster_name'] = poster_path_rel
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    # Call insert_book from db.py with all 4 fields
    book_id = insert_book(
        data['name'],
        data['description'],
        url_path,
        poster_path_rel
    )

    return jsonify({
        'message': f'PDF and JSON saved successfully with DB id {book_id}',
        'pdf_file': pdf_filename,
        'json_file': json_filename,
        'poster_name': poster_path_rel,
        'db_id': book_id
    }), 200
@app.route('/rows')
def rows():
    data = getrows()
    return jsonify(data)

@app.route('/fetch/<int:page>')
def fetch_page(page):
    per_page = 20

    # Call your getinfo() that returns JSON string of all rows
    all_data_json = getinfo()

    # Parse JSON string into Python list of dicts
    all_data = json.loads(all_data_json)

    start = (page - 1) * per_page
    end = start + per_page

    # Slice the data for current page
    page_data = all_data[start:end]

    return jsonify(page_data)
# your /download endpoint remains unchanged
@app.route('/files/<path:filename>')
def serve_file(filename):
    # Securely join the path to prevent directory traversal attacks
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Check if the file exists and is inside UPLOAD_FOLDER
    if os.path.isfile(full_path) and os.path.commonpath([os.path.abspath(full_path), os.path.abspath(UPLOAD_FOLDER)]) == os.path.abspath(UPLOAD_FOLDER):
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        abort(404)



@app.route('/detail/<int:number>')
def get_detail(number):
    try:
        # Assuming getinfo() returns all data as JSON string
        all_data = json.loads(getinfo())

        # Search for the row with id == number
        for item in all_data:
            if int(item.get("id", -1)) == number:
                return jsonify(item)

        # If not found
        return jsonify({'error': f'No item found with id {number}'}), 404

    except Exception as e:
        return jsonify({'error': f'Failed to get detail: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
