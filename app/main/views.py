"""
    Blueprint for main routes and views
"""
# from datetime import datetime
from flask import render_template, session, redirect, url_for
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
    """Register page view."""
    form = RegisterForm()
    if form.validate_on_submit():
        # Add the new user to the database
        new_user = User(username=form.username.data, password=form.password.data, pin=form.pin.data)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        return redirect(url_for('.index'))
    return render_template('register.html', form=form)
