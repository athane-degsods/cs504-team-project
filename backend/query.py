"""Querying module for the authentication database."""
import sqlite3

def get_user_by_username(username):
    """Fetches a user from the database by username."""
    print(f"Fetching user by username: {username}")

    conn = sqlite3.connect('database/auth.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
    user = cursor.fetchone()

    print(f"Fetched user from database: {user}")

    conn.close()

    return user

def create_user(username, password, PIN):
    """Create a new user in the database."""
    try:
        print(f"Creating user: {username}, {password}, {PIN}")

        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO users (username, password, PIN) VALUES (?, ?, ?)""", (username, password, PIN))
        conn.commit()

        print(f"User created successfully: {username}")

        return True, "User created successfully"

    except sqlite3.IntegrityError as e:
        print(f"Error creating user: {e}")
        return False, str(e)

    finally:
        conn.close()
