"""
    This script contains the forms used in the application.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length , Regexp, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    """
        Login form
        Validators:
            1. Username:
                - DataRequired: Ensure that the field is not empty
                - Length: Ensure that the input length is within a (1, 64) range
                - Regexp: Ensure that the input matches a specific regular expression pattern
            2. Password:
                - DataRequired: Ensure that the field is not empty
            3. PIN:
                - DataRequired: Ensure that the field is not empty
    """
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # pin = PasswordField('PIN', validators=[DataRequired()])
    # submit = SubmitField('login')
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(1, 64, message="Username must be between 1 and 64 characters."),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
    ])
    pin = PasswordField('PIN', validators=[
        DataRequired(message="PIN is required."),
    ])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    """
        Register form
        Validators:
            1. Username:
                - DataRequired: Ensure that the field is not empty
                - Length: Ensure that the input length is within a (1, 64) range
                - Regexp: Ensure that the input matches a specific regular expression pattern
            2. Password:
                - DataRequired: Ensure that the field is not empty
                - EqualTo: Ensure that the input matches the value of repeat_password field
            3. Repeat Password:
                - DataRequired: Ensure that the field is not empty
            4. PIN:
                - DataRequired: Ensure that the field is not empty
    """
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # repeat_password = PasswordField('Repeat Password', validators=[DataRequired()])
    # pin = PasswordField('PIN', validators=[DataRequired()])
    # submit = SubmitField('register')
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(1, 64, message="Username must be between 1 and 64 characters."),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        EqualTo('repeat_password', message="Passwords must match."),
    ])
    repeat_password = PasswordField('Repeat Password', validators=[
        DataRequired(message="Please repeat your password."),
    ])
    pin = PasswordField('PIN', validators=[
        DataRequired(message="PIN is required."),
    ])
    submit = SubmitField('Register')

    def validate_username(self, field):
        """Validate username"""
        if User.query.filter_by(username=field.data).first():
            raise ValueError('Username already in use.')
