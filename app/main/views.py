"""
    Blueprint for main routes and views
"""
# from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import LoginForm, RegisterForm
from .. import db
from ..models import User
from ..orm_query import find_user_by_username, create_user
from ..utils import hash_string, compare_input_to_stored_hash

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     """Login page view."""
#     form = LoginForm()
#     if form.validate_on_submit():
#         return redirect(url_for('.index'))
#     return render_template('index.html',
#                            form=form, name=session.get('name'),
#                            known=session.get('known', False),
#                            current_time=datetime.utcnow())

@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login page view."""
    form = LoginForm()
    print(f"Form data: username={form.username.data}, password={form.password.data}, pin={form.pin.data}")
    if form.validate_on_submit():
        # Check if the user exists in the database

        # Hash both pin and password for security purpose
        password = form.password.data
        pin = form.pin.data
        username = form.username.data

        # Create a dictionary to hold the authentication status
        auth_status = {
            "is_user_exist": False,
            "is_password_correct": False,
            "is_pin_correct": False
        }

        # Check if the user exists in the database
        user = find_user_by_username(username)
        if user:
            auth_status["is_user_exist"] = True
            print(f"User found: {user.username}")
        else:
            return render_template('login.html', form=form, error="User does not exist.")

        if compare_input_to_stored_hash(password, user.password):
            print("Comparing stored hashed password and input hashed password")
            auth_status["is_password_correct"] = True
            print("Password is correct")
        else:
            return render_template('login.html', form=form, error="Incorrect password.")

        if compare_input_to_stored_hash(pin, user.pin):
            auth_status["is_pin_correct"] = True
            print("PIN is correct")
        else:
            return render_template('login.html', form=form, error="Incorrect PIN.")

        if all(auth_status.values()):
            print("All authentication checks passed. User is authenticated.")
            return redirect(url_for('.index'))

    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    """
        Register page view.
        The flow of this function is:
        Create an instance of the RegisterForm -> Validate the form
        -> If valid, hash the password and check if the username already exists in the database
        -> If the username is not taken, create a new user and add it to the database
        -> Redirect to the login page
    """
    form = RegisterForm()
    print(f"Form data: username={form.username.data}, password={form.password.data}, pin={form.pin.data}")
    if form.validate_on_submit():
        print("Form is valid -> Hashing password")
        print(f"Form data: username={form.username.data}, password={form.password.data}, pin={form.pin.data}")
        print(f"Form data types: username={type(form.username.data)}, password={type(form.password.data)}, pin={type(form.pin.data)}")
        username = form.username.data
        hashed_password = hash_string(form.password.data)
        hashed_pin = hash_string(form.pin.data)
        print(f"Password is hashed from {form.password.data} to {hashed_password}")
        print(f"PIN is hashed from {form.pin.data} to {hashed_pin}")
        print(f"Checking if username {form.username.data} already exists")
        existing_user = find_user_by_username(form.username.data)
        if existing_user:
            print("Username already exists")
            form.username.errors.append('Username already exists.')
        else:
            print(f"type of username: {type(username)}, type of hashed_password: {type(hashed_password)}, type of hashed_pin: {type(hashed_pin)} after user existence check")
            print("Username is available -> Creating new user")
            create_user(username, hashed_password, hashed_pin)
            print(f"New user created: {username}")
            return redirect(url_for('.login'))
    else:
        print("Form is not valid")
        print(f"Form errors: {form.errors}")
    return render_template('register.html', form=form)

@main.route('/')
def index():
    """Index page view."""
    return render_template('index.html')