
# /RfMRI/src/api/routes.py

from flask import Blueprint, request, jsonify, abort
from src.api.auth import authenticate, authorize
from src.core.analysis_engine import AnalysisEngine
from src.core.data_processor import DataProcessor, FeatureExtractor
from src.db.models import User, MRIAnalysis
from src.db.database import add_entity, db_session

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/user/create', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        abort(400, description="Missing username or password.")
    
    # Assume password is already hashed from the client side for this example
    new_user = User(username=data['username'], hashed_password=data['password'])
    add_entity(new_user)
    return jsonify({"message": "User created successfully.", "user_id": new_user.id}), 201

@api_blueprint.route('/mri/analyze', methods=['POST'])
@authenticate
def analyze_mri_data():
    """Analyze MRI data."""
    user = request.g.user
    data = request.get_json()
    if not data:
        abort(400, description="No MRI data provided.")

    try:
        processor = DataProcessor(data)
        processed_data = processor.preprocess()
        features = FeatureExtractor(processed_data).extract_features()
        engine = AnalysisEngine(features)
        results = engine.analyze()
        
        new_analysis = MRIAnalysis(user_id=user.id, result=str(results))
        add_entity(new_analysis)
        
        return jsonify(results), 200
    except Exception as e:
        abort(500, description=str(e))

@api_blueprint.route('/user/<int:user_id>/analyses', methods=['GET'])
@authenticate
@authorize(roles=['admin', 'user'])
def get_user_analyses(user_id):
    """Retrieve all analyses for a given user."""
    if request.g.user.id != user_id and request.g.user.role != 'admin':
        abort(403, description="Unauthorized to view these records.")
    
    analyses = db_session.query(MRIAnalysis).filter_by(user_id=user_id).all()
    return jsonify([{'id': analysis.id, 'result': analysis.result, 'date': analysis.analysis_date} for analysis in analyses]), 200
    