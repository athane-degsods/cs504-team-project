"""
    Application script
"""
import os
import unittest

from app import create_app, db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """
        Return a dictionary of items to be automatically imported into the shell session.
    """
    return dict(db=db, User=User)

@app.cli.command()
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
