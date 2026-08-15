# Transitioning to SQLAlchemy ORM
from app.models import User
from app import db 

def find_user_by_username(username):
    """refined function to find a user by username"""
    user = User.query.filter_by(username=username).first()
    return user

def create_user(username, password, PIN):
    """Create a new user in the database"""
    print(f"create_user invoked with username: {username}, hashed password: {password}, hashed PIN: {PIN}")
    print(f"type of username: {type(username)}, type of password: {type(password)}, type of PIN: {type(PIN)}")
    user = User(username=username, password=password, pin=PIN)
    print("adding user to the database session")
    db.session.add(user)
    print("db.session.add(user) executed")
    db.session.commit()
    print("db.session.commit() executed")
    print("successfully committed the new user to the database")
    return user



# user=User(username="testuser", password="b'$2b$12$nXw0hivWbf5XaTDm4ywFa.cIQDScXwcBQ7ToBj6zlYxgso9OHtBwe'", pin="b'$2b$12$nXw0hivWbf5XaTDm4ywFa.cIQDScXwcBQ7ToBj6zlYxgso9OHtBwe'")