
# /RfMRI/src/api/error_handlers.py

from flask import jsonify
from werkzeug.exceptions import HTTPException

def handle_errors(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify(error=str(e.description)), e.code
        return jsonify(error="Internal Server Error"), 500
    