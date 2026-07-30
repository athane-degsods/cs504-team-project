"""This module contains utility functions for the backend."""
import bcrypt

def tuple_to_dict(tuple_values, arr_keys):
    """Convert a tuple to a dictionary using the provided keys."""

    d = {}

    print(f"length of tuple_values: {len(tuple_values)}")
    print(f"length of arr_keys: {len(arr_keys)}")

    if len(tuple_values) == len(arr_keys):
        for i, arr_key in enumerate(arr_keys):
            d[arr_key] = tuple_values[i]

    return d

def hash_password(password):
    """Hashes the password using a simple hashing algorithm."""

    bytes_password = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(bytes_password, salt)

    print(f"Password: {password}")
    print(f"Salt: {salt}")
    print(f"Password hashed: {hashed_password}")

    return hashed_password

def check_password(input_password, stored_hashed_password):
    """Check if the input password matches the stored hashed password."""
    print(f"stored_hashed_password: {stored_hashed_password}")

    try:
        bytes_input_password = input_password.encode('utf-8')

        is_valid = bcrypt.checkpw(bytes_input_password, stored_hashed_password)
        return is_valid

    except (ValueError, TypeError):
        return False
