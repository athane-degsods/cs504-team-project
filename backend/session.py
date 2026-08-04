"""This module handles user session management"""
from datetime import datetime, timezone, timedelta
from functools import wraps
import jwt
from flask import request, jsonify

SECRET_KEY = 'mysecretkey'  # This should be stored in an environment variable

def generate_token(username):
    """Generates a JWT token for the given user."""

    alg='HS256' # algorithm used for encoding the token
    iat = datetime.now(timezone.utc)  # issued at time
    nbf = iat  # not before time
    exp = iat + timedelta(hours=1)  # expiration time (1 hour from now)

    print("Token generation ingredients: ")
    print(f"username: {username}")
    print(f"SECRET_KEY: {SECRET_KEY}")
    print(f"algorithm: {alg}")
    print(f"issued at: {iat}")
    print(f"not before: {nbf}")
    print(f"expiration: {exp}")

    # token = jwt.encode({
    #     'username': username
    # }, SECRET_KEY, algorithm=alg)

    payload = {
        'sub': username,
        'iat': iat,
        'nbf': nbf,
        'exp': exp
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=alg)

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
            current_user = data['sub']
            iat = data['iat']
            nbf = data['nbf']
            exp = data['exp']
        except jwt.exceptions.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, iat, nbf, exp, *args, **kwargs)

    return decorated

# def decoder(token):
#     """test module for decorator"""

#     data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

#     print(f"Decoded token data: {data}")

#     return

# token = generate_token("testuser")
# decoder(token)