
# /RfMRI/src/api/health.py

from flask import Blueprint, jsonify

health_blueprint = Blueprint('health', __name__)

@health_blueprint.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to ensure the API is operational."""
    return jsonify({'status': 'healthy'}), 200
    