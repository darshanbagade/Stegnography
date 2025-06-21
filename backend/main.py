from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from encrypt import encode_text
from decrypt import decode_text
from flask_cors import CORS
import time

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploaded')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    image = request.files.get('image')
    secret = request.form.get('secret')
    password = request.form.get('password')

    if not (image and allowed_file(image.filename) and secret and password):
        return jsonify({'error': 'Invalid file or missing data'}), 400

    filename = secure_filename(image.filename)
    # Add timestamp to avoid overwrite
    base, ext = os.path.splitext(filename)
    filename = f"{base}_{int(time.time())}{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted_' + filename)
    try:
        encode_text(filepath, output_path, secret, password)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return send_file(output_path, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    image = request.files.get('image')
    password = request.form.get('password')

    if not (image and allowed_file(image.filename) and password):
        return jsonify({'error': 'Invalid file or password'}), 400

    filename = secure_filename(image.filename)
    base, ext = os.path.splitext(filename)
    filename = f"{base}_{int(time.time())}{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    try:
        hidden_msg = decode_text(filepath, password)
        return jsonify({'message': hidden_msg})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)