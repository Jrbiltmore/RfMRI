
# /RfMRI/src/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from src.api.auth import authenticate, authorize
from src.core.data_processor import DataProcessor
from src.utils.logger import setup_logging
from src.db.database import initialize_db
from src.core.analysis_engine import AnalysisEngine

app = Flask(__name__)
CORS(app)
setup_logging()

@app.route('/api/analyze', methods=['POST'])
@authenticate
@authorize
def analyze_data():
    """Endpoint to process MRI data and return analysis results."""
    data = request.get_json()
    if not data:
        app.logger.error("No data provided")
        return jsonify({"error": "No data provided"}), 400

    try:
        processor = DataProcessor(data)
        processed_data = processor.process()
        analysis_engine = AnalysisEngine(processed_data)
        results = analysis_engine.analyze()
        return jsonify({"results": results}), 200
    except Exception as e:
        app.logger.exception("Failed to analyze data")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to ensure the API is operational."""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    initialize_db(app.config['DATABASE_URI'])
    app.run(debug=False, host='0.0.0.0', port=5000)
