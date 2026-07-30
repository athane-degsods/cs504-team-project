"""This module handles user session management"""
# from datetime import datetime, timezone, timedelta
import jwt
from flask import request, jsonify
from functools import wraps

SECRET_KEY = 'mysecretkey'  # This should be stored in an environment variable

def generate_token(username):
    """Generates a JWT token for the given user."""

    token = jwt.encode({
        'username': username
    }, SECRET_KEY, algorithm='HS256')

    return token

def token_required(f):
    """Decorator to ensure that a valid token is submitted"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['username']
        except jwt.exceptions.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
