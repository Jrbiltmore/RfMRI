
# /RfMRI/src/api/auth.py

from functools import wraps
from flask import request, jsonify, g
import jwt
import datetime
from werkzeug.security import check_password_hash
from src.db.models import User
from src.db.database import db_session

SECRET_KEY = 'your_secret_key_here'  # Ideally, this should be in a secure, environment-specific config

def authenticate(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Missing token.'}), 403

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = db_session.query(User).filter_by(id=payload['sub']).first()
            if not user:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired.'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token.'}), 403

        g.user = user
        return func(*args, **kwargs)
    return decorated_function

def authorize(roles):
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if g.user.role not in roles:
                return jsonify({'message': 'Permission denied.'}), 403
            return func(*args, **kwargs)
        return decorated_function
    return wrapper

def generate_token(user_id, expires_in=3600):
    """Generate an authentication token."""
    payload = {
        'sub': user_id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

def verify_password(username, password):
    """Verify user password."""
    user = db_session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.hashed_password, password):
        return user
    return None
    