"""
Models for SQLAlchemy
"""
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

from . import db
from . import login_manager
from .utils import hash_string, compare_input_to_stored_hash

class User(db.Model, UserMixin):
    """User model"""
    # define the table name
    __tablename__ = 'users'

    # Define the columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    # pin_hash = db.Column(db.Text, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=False, nullable=False) # Flip unique to False during development

    # second factor PIN
    pin = db.Column(db.String(6), nullable=True)
    pin_expiration = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """Return a string of the user's username"""
        return f'<User {self.username}>'

    # Password property and setter
    @property
    def password(self):
        """
            @property decorator ensure that this is a standard attribute.
            You can access the value but you cannot set it directly.
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = hash_string(password)

    def verify_password(self, password):
        """Verify the password against the stored hash"""
        return compare_input_to_stored_hash(password, self.password_hash)

    # # Pin property and setter
    # @property
    # def pin(self):
    #     """
    #         @property decorator ensure that this is a standard attribute.
    #         You can access the value but you cannot set it directly.
    #     """
    #     raise AttributeError('pin is not a readable attribute.')

    # @pin.setter
    # def pin(self, pin):
    #     self.pin_hashed = hash_string(pin)

    # def verify_pin(self, pin):
    #     """Verify the pin against the stored hash"""
    #     return compare_input_to_stored_hash(pin, self.pin_hashed)

    # Verification methods
    def generate_verification_token(self):
        """
            Generate a token for email verification.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'verify': self.id})

    # convert this method to a static method since it does not depend on the User instance.
    @staticmethod
    def verify_token(token, expiration=3600):
        """
            Verify the token for email verification.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # Decode the token
            data = s.loads(token, max_age=expiration)
        except:
            return False

        # Extract the user ID from the token and return the user object
        user = User.query.get(data.get('verify'))
        return user


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID"""
    return User.query.get(int(user_id))
