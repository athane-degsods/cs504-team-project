import pytest
from app import create_app, db

@pytest.fixture
def test_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all() # create the database tables (nothing will be created if the tables already exist)
        yield app # pause here and let the test run
        db.drop_all() # drop the database tables after the test is done
