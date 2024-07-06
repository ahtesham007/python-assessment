from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

# Improved logging configuration with docstring and exception handling
def configure_logging():
    """
    Configures logging for the application. Sets up a console handler and a file handler.

    Raises:
        ImportError: If an error occurs while importing the logging module.
    """
    try:
        from logging.config import dictConfig
    except ImportError:
        raise ImportError("Failed to import logging module. Please ensure it's installed.")

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "default",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": "app.log",
                    "formatter": "default",
                },
            },
            "root": {"level": "DEBUG", "handlers": ["console", "file"]},
        }
    )

configure_logging()

# Create the Flask application with docstring and exception handling
def create_app():
    """
    Creates and configures a Flask application instance.

    Raises:
        ImportError: If an error occurs while importing necessary modules.
    """
    try:
        app = Flask(__name__)
        app.config.from_object(Config)

        db.init_app(app)

        jwt = JWTManager(app)  # Initialize JWTManager

        with app.app_context():
            from . import routes  # Import routes blueprint
            from . import auth   # Import auth blueprint
            from .models import User, Product  # Import models

            db.create_all()  # Create database tables (if not already exist)

            app.register_blueprint(routes.main_bp)
            app.register_blueprint(auth.auth_bp)

        return app
    except ImportError as e:
        app.logger.error(f"Error creating app: {e}")
        raise
