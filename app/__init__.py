"""
    This module creates and configures the Flask application instance
"""

from flask_login import LoginManager

from flask_mail import Mail

from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = 'main.login'

def create_app(config_name):
    """
        An app instance is created and configured based on the provided settings from config.py.
        A db instance is also initialized helps handling database operations.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name]) # ingest the configurations
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
