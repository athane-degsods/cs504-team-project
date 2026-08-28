"""
    Blueprint for main routes and views
"""
# from datetime import datetime
from flask import flash, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user
from . import main
from .forms import LoginForm, RegisterForm
from .. import db
from ..models import User

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
    # form = LoginForm()
    # if form.validate_on_submit():
        # # Check if the user exists in the database

        # # Hash both pin and password for security purpose
        # password = form.password.data
        # pin = form.pin.data
        # username = form.username.data

        # # Create a dictionary to hold the authentication status
        # auth_status = {
        #     "is_user_exist": False,
        #     "is_password_correct": False,
        #     "is_pin_correct": False
        # }

        # # Check if the user exists in the database
        # user = find_user_by_username(username)
        # if user:
        #     auth_status["is_user_exist"] = True
        #     print(f"User found: {user.username}")
        # else:
        #     return render_template('login.html', form=form, error="User does not exist.")

        # if compare_input_to_stored_hash(password, user.password):
        #     print("Comparing stored hashed password and input hashed password")
        #     auth_status["is_password_correct"] = True
        #     print("Password is correct")
        # else:
        #     return render_template('login.html', form=form, error="Incorrect password.")

        # if compare_input_to_stored_hash(pin, user.pin):
        #     auth_status["is_pin_correct"] = True
        #     print("PIN is correct")
        # else:

        #     return render_template('login.html', form=form, error="Incorrect PIN.")

        # if all(auth_status.values()):
        #     print("All authentication checks passed. User is authenticated.")
        #     login_user(user)
        #     return redirect(url_for('.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        user_exists = user is not None
        password_verified = user.verify_password(form.password.data)
        pin_verified = user.verify_pin(form.pin.data)
        if user_exists and password_verified and pin_verified:
            login_user(user)
            # `next_url` is implemented so that when the user try to access a protected page,
            # they are redirected to that page after login.
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for('.index')
            return redirect(next_url)
        flash('Invalid username, password, or PIN.')
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
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
            pin=form.pin.data
        )
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login!')
        return redirect(url_for('main.login'))
    else:
        print("Form is not valid")
        print(f"Form errors: {form.errors}")
        flash(f"Form errors: {form.errors}")
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    """Logout user endpoint."""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.index'))

@main.route('/')
@login_required
def index():
    """Index page view."""
    return render_template('index.html')
