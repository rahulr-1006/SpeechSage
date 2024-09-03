# utils.py
import os
from werkzeug.utils import secure_filename
import logging

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_dir):
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    logging.info(f"File saved to {filepath}")
    return filepath

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory {directory}")
