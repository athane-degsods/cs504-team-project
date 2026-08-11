"""
Models for SQLAlchemy
"""
from . import db

class User(db.Model):
    """User model"""
    # define the table name
    __tablename__ = 'users'

    # Define the columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    pin = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        """Return a string of the user's username"""
        return f'<User {self.username}>'
