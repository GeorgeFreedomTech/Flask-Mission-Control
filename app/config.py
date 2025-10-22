"""
Configuration settings for the Flask application.

    BaseConfig for common settings.
    DevConfig for development & testing configurations.
    ProdConfig for production configurations.
"""
import os
from dotenv import load_dotenv


# Find the absolute path of the root directory of the app
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file
load_dotenv(os.path.join(basedir, '..', '.env'))

class BaseConfig:
    """Base configuration."""
    APP_ENV = "base configuration"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.environ.get('DATABASE_FILE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    """Development configuration."""
    APP_ENV = "development"
    DEBUG = True


class ProdConfig(BaseConfig):
    """Production configuration."""
    # In a real production environment, these variables would be set
    # directly on the server, not from a .env file.
    pass