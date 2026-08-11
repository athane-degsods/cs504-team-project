"""
    This script contains the forms used in the application.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    pin = PasswordField('PIN', validators=[DataRequired()])
    submit = SubmitField('login')

class RegisterForm(FlaskForm):
    """Register form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired()])
    pin = PasswordField('PIN', validators=[DataRequired()])
    submit = SubmitField('register')
