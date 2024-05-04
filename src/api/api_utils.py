
# /RfMRI/src/api/api_utils.py

def validate_request(req_data, required_fields):
    """Utility function to validate required fields in an API request."""
    missing_fields = [field for field in required_fields if field not in req_data]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"
    return True, ""

def respond_with_error(message, status_code):
    """Utility function to create an error response for API calls."""
    return {'error': message}, status_code
    