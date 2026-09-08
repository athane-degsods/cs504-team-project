"""
    This script contains the forms used in the application.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length , Regexp, EqualTo, Email

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
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    """
        Register form
        Validators:
            1. Username:
                - DataRequired: Ensure that the field is not empty
                - Length: Ensure that the input length is within a (1, 64) range
            2. Password:
                - DataRequired: Ensure that the field is not empty
                - EqualTo: Ensure that the input matches the value of repeat_password field
            3. Repeat Password:
                - DataRequired: Ensure that the field is not empty
    """
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # repeat_password = PasswordField('Repeat Password', validators=[DataRequired()])
    # pin = PasswordField('PIN', validators=[DataRequired()])
    # submit = SubmitField('register')
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(1, 64, message="Username must be between 1 and 64 characters.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        EqualTo('repeat_password', message="Passwords must match."),
    ])
    repeat_password = PasswordField('Repeat Password', validators=[
        DataRequired(message="Please repeat your password."),
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Length(1, 120, message="Email must be between 1 and 120 characters."),
        Email(message="Invalid email address."), # notice the user on invalid email address
    ])
    submit = SubmitField('Register')

    def validate_username(self, field):
        """Validate username"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        """Validate email"""
        if User.query.filter_by(email=field.data).first():
            # more information about validationerror here: https://wtforms.readthedocs.io/en/2.3.x/validators/
            raise ValidationError('Email already in use.')


class VerifyPinForm(FlaskForm):
    """
        Verify PIN form.
    """
    input = StringField('PIN', validators=[
        DataRequired(message="PIN is required."),
        Length(6, 6, message="PIN must be exactly 6 digits."),
        Regexp('^[0-9]{6}$', 0, 'PIN must consist of exactly 6 digits.')
    ])
    submit = SubmitField('Verify PIN')
