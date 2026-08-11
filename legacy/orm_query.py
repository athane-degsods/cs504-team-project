# Transitioning to SQLAlchemy ORM
from app.models import User
from legacy.flasky import db

def find_user_by_username(username):
    """refined function to find a user by username"""
    user = User.query.filter_by(username=username).first()
    return user

def create_user(username, password, PIN):
    """Create a new user in the database"""
    user = User(username=username, password=password, PIN=PIN)
    db.session.add(user)
    db.session.commit()
    return user
