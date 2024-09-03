# main.py
from flask import request, jsonify
from . import app
from .utils import allowed_file, save_uploaded_file
from .analysis import convert_speech_to_text, analyze_speech, detailed_speech_analysis
import os
import datetime
import logging

# Logger setup
logging.basicConfig(filename='speechsage.log', level=logging.INFO)

@app.route('/upload', methods=['POST'])
def upload_speech():
    if 'file' not in request.files:
        logging.error("No file part in the request.")
        return jsonify({"error": "No file part in the request."}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        logging.error("No selected file.")
        return jsonify({"error": "No selected file."}), 400
    
    if file and allowed_file(file.filename):
        filepath = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        
        logging.info(f"File saved to {filepath}")
        
        transcript = convert_speech_to_text(filepath)
        analysis = analyze_speech(transcript)
        
        response = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "filename": os.path.basename(filepath),
            "transcript": transcript,
            "analysis": analysis
        }
        
        logging.info(f"Analysis complete for {filepath}")
        return jsonify(response), 200
    
    logging.error("Invalid file type.")
    return jsonify({"error": "Invalid file type."}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "timestamp": datetime.datetime.utcnow().isoformat()}), 200

@app.route('/detailed-analysis', methods=['POST'])
def detailed_analysis():
    data = request.json
    transcript = data.get("transcript", "")
    
    if not transcript:
        logging.error("No transcript provided for detailed analysis.")
        return jsonify({"error": "No transcript provided."}), 400
    
    detailed_results = detailed_speech_analysis(transcript)
    
    logging.info("Detailed analysis completed.")
    return jsonify(detailed_results), 200
