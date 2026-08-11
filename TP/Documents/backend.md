https://flask.palletsprojects.com/en/stable/quickstart/

The user from the database is fetched as a tuple. So I think a normalization function to convert the tuple to a dictionary would be helpful. This way, I can access the user data using keys instead of indices, making the code more readable and maintainable.

Using bcrypt for password hashing in python: https://www.geeksforgeeks.org/python/hashing-passwords-in-python-with-bcrypt/

JWT is used to manage user's session: https://www.jwt.io/

Sample code for JWT in python: https://www.geeksforgeeks.org/python/using-jwt-for-user-authentication-in-flask/

sample jwt 
```python
import jwt

def generate_token(username):
    """Generates a JWT token for the given user."""
    secret_key = 'mysecretkey' # should be stored in the environment variable

    token = jwt.encode({
        'username': username
    }, secret_key, algorithm='HS256')

    return token

print(f"Token generated: {generate_token('testuser')}")
# Token generated: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIn0.J7p353n90GM_SklFUb2M-z__o0lGAKjxym5h5DzTcpw
```
![1785278971995](image/backend/1785278971995.png)

more about jwt functionality: https://trstringer.com/jwt-authz-identity-provider-flow/