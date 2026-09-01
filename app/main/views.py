"""
    Blueprint for main routes and views
"""
# from datetime import datetime
from datetime import datetime, timedelta, timezone
import secrets

from flask import flash, request, render_template, redirect, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.email import send_email
from . import main
from .forms import LoginForm, RegisterForm, VerifyPinForm
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
        # pin_verified = user.verify_pin(form.pin.data)
        email_verified = user.verified if user_exists else False

        if user_exists and password_verified and email_verified:
            pin = ''.join([str(secrets.randbelow(10)) for i in range(6)])
            expiration = datetime.now(timezone.utc) + timedelta(minutes=5)
            print(f"Generated PIN: {pin}, Expiration: {expiration}")
            user.pin = pin
            user.pin_expiration = expiration
            db.session.commit()

            # Send the PIN to the user's email
            send_email(user.email, "Your PIN for 2FA", 'email/pin', user=user, pin=pin)
            flash('A PIN has been sent to your email.')

            # assign a temporary session variable to track the user for PIN verification
            session['pin_verifying_user_id'] = user.id

            return redirect(url_for('main.verify_pin'))


        # if user_exists and password_verified and email_verified:
        #     login_user(user)
        #     # `next_url` is implemented so that when the user try to access a protected page,
        #     # they are redirected to that page after login.
        #     next_url = request.args.get('next')
        #     if next_url is None or not next_url.startswith('/'):
        #         next_url = url_for('.index')
        #     return redirect(next_url)
        # flash('Invalid username, password, or PIN.')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    """
        Register page view.
        The flow of this function is:
        Create an instance of the RegisterForm -> Validate the form
        -> If valid, hash the password and check if the username already exists in the database
        -> If the username is not taken, create a new user and add it to the database
        -> Send a verification email to the user with a token that expires in 60 minutes
        -> Redirect to the login page
    """
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()

        # Send verification email
        token = user.generate_verification_token()
        send_email(user.email, "Confirm your email address",
                   'email/verify', user=user, token=token)
        flash('A verification email has been sent to your email address.')
        return redirect(url_for('main.login'))
    else:
        print("Form is not valid")
        print(f"Form errors: {form.errors}")
        flash(f"Form errors: {form.errors}")
    return render_template('register.html', form=form)

@main.route('/verify_pin', methods=['GET', 'POST'])
def verify_pin():
    form = VerifyPinForm()
    if form.validate_on_submit():
        user_id = session.get('pin_verifying_user_id')
        if not user_id:
            flash('No user is currently in the process of PIN verification.')
            return redirect(url_for('main.login'))

        user = User.query.get(user_id)
        if not user:
            flash('User not found.')
            return redirect(url_for('main.login'))

        # Strip off timezone information to avoid comparison issues.
        current_time = datetime.now(timezone.utc).replace(tzinfo=None)
        print(f"Current time: {current_time}, User's PIN expiration: {user.pin_expiration}")

        if user.pin == form.input.data and current_time < user.pin_expiration:
            login_user(user)
            session.pop('pin_verifying_user_id', None)  # Clear the session variable
            flash('You have been logged in successfully.')

            # route the user to the next page or the index page.
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for('.index')
            return redirect(next_url)
        else:
            flash('Invalid PIN or PIN has expired.')
    return render_template('verify_pin.html', form=form)


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

# @main.route('/verify/<token>')
# def verify(token):
#     """
#     Verify the user's email address using the provided token.
#     """
#     if current_user.verified:
#         return redirect(url_for('main.index'))
#     if current_user.verify_token(token):
#         db.session.commit()
#         flash('You have verified your account. Thanks!')
#     else:
#         flash('The confirmation link is invalid or has expired.')
#     return redirect(url_for('main.index'))

# Redevelop /verify/<token> route to handle email verification without the need of user logging in.
@main.route('/verify/<token>')
def verify(token):
    """
       This is the verify route
       The user is extracted from the token and verified without the need of logging in.
    """
    user = User.verify_token(token)

    if user is None:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('main.login'))

    if user.verified:
        flash('Your account is already verified, please login.')
    else:
        user.verified = True
        db.session.commit()
        flash('You have verified your account. Please login.')

    return redirect(url_for('main.login'))


@main.before_app_request
def before_request():
    """
       before_app_request hook checks if the user is authenticated and if their email is verified.
    """
    if current_user.is_authenticated \
            and not current_user.verified \
            and request.blueprint != 'main' \
            and request.endpoint != 'static':
        return redirect(url_for('main.unverified'))

@main.route('/unverified')
def unverified():
    """
        Unverified page view.
    """
    if current_user.is_anonymous or current_user.verified:
        return redirect(url_for('main.index'))
    return render_template('main/unconfirmed.html')

@main.route('/reverify')
@login_required
def reverify():
    """
        Resend the verification email to the user.    
    """
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'email/verify', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
