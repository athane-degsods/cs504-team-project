"""Important modules and initializes the Flask application."""

from flask import Flask, render_template, request, make_response
from backend.query import get_user_by_username, create_user
from backend.utils import tuple_to_dict, hash_password, check_password
from backend.session import generate_token, token_required

app = Flask(__name__)

def validate_password(input_password, auth_state, user=None):
    """Validates the input password against the database password."""
    print(f"password state: {auth_state['valid_password']}")
    print(f"Validating password: {input_password}")

    if check_password(input_password, user["password"]):
        auth_state["valid_password"] = True

    return auth_state

def validate_PIN(input_PIN, auth_state, user=None):
    """Validates the input PIN against the database PIN."""
    print(f"Validating PIN: {input_PIN}")
    if input_PIN == user["PIN"]:
        auth_state["valid_PIN"] = True
    return auth_state


def validate_username(input_username, auth_state):
    """Updates the username in the authentication state."""
    print(f"Updating username: {input_username}")
    auth_state["username"] = input_username
    return auth_state

def validate_authentication(auth_state, user=None):
    """Check if the auth_state is valid for authentication."""
    print(f"Validating authentication: {auth_state}")
    if (
        auth_state["valid_password"] and
        auth_state["valid_PIN"] and
        auth_state["username"] == user["username"]
    ):
        auth_state["authenticated"] = True
        token = generate_token(auth_state["username"])
        print(f"Token generated: {token}")

    return auth_state, token

@app.route("/")
def hello_world():
    """"Simple route that returns a greeting message."""
    return "<p>Hello, World!</p>"

@app.route('/login', methods=['POST'])
def login():
    """Route for the login page."""
    data = request.get_json()
    print("ENTER BACKEND LOGIC")
    print(f"Received request: {request}")
    print(f"Received data: {data}")

    auth_state = {
        "username": None,
        "valid_password": False,
        "valid_PIN": False,
        "authenticated": False
    }
    user = get_user_by_username(data.get("username"))

    if user is None:
        return {'message': 'User not found', "data": data}, 401

    dict_user = tuple_to_dict(user, ["id", "username", "password", "PIN"])

    print(f"User fetched from database: {user}")
    print(f"User converted to dictionary: {dict_user}")

    validate_username(data.get("username"), auth_state)
    validate_password(data.get("password"), auth_state, dict_user)
    validate_PIN(data.get("PIN"), auth_state, dict_user)

    auth_state, token = validate_authentication(auth_state, dict_user)

    if auth_state["authenticated"]:
        response = make_response({'message': 'Login successful', "data": data})
        response.set_cookie('jwt_token', token)
        return response, 200

    return {'message': 'Invalid credentials', "data": data}, 401

@app.route('/login', methods=['GET'])
def login_get():
    """Route for the login page"""
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register_get():
    """Route for the register page"""
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    print(f"Received registration data: {data}")

    print(f"password: {data.get('password')}")

    hashed_password = hash_password(data.get("password"))

    if not create_user(data.get("username"), hashed_password, data.get("PIN"))[0]:
        return {'message': 'User already exists', "data": data}, 400

    return {'message': 'Registration successful', "data": data}, 200

@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard(current_user):
    """Route for the dashboard page."""
    print(f"Accessing dashboard for user: {current_user}")

    return render_template('dashboard.html')
