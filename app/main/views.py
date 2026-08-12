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
from ..utils import hash_password, check_password

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
    if form.validate_on_submit():
        # Check if the user exists in the database
        print(f"Form data: username={form.username.data}, password={form.password.data}, pin={form.pin.data}")
        user = User.query.filter_by(username=form.username.data).first()
        print(f"User fetched from database: {user}")
        if user and user.password == form.password.data and user.pin == form.pin.data:
            session['username'] = user.username
            return redirect(url_for('.index'))
        print(f"Session data after login attempt: {session}")
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
        hashed_password = hash_password(form.password.data)
        hashed_pin = hash_password(form.pin.data)
        print(f"Password is hashed from {form.password.data} to {hashed_password}")
        print(f"PIN is hashed from {form.pin.data} to {hashed_pin}")
        print(f"Checking if username {form.username.data} already exists")
        existing_user = find_user_by_username(form.username.data)
        if existing_user:
            print("Username already exists")
            form.username.errors.append('Username already exists.')
        else:
            print("Username is available -> Creating new user")
            new_user = User(username=form.username.data, password=hashed_password, pin=hashed_pin)
            create_user(new_user, hashed_password, hashed_pin)
            print(f"New user created: {new_user}")
    else:
        print("Form is not valid")
        print(f"Form errors: {form.errors}")
    return render_template('register.html', form=form)
