"""
This is the main application package for the Flask To-Do App.

This package uses the Application Factory pattern to create and configure
the Flask app instance.

It initializes the following components:
- SQLAlchemy for database connection from 'extensions.py'.
- Bcrypt for password hashing from 'extensions.py'.
- LoginManager for user session management from 'extensions.py'.
It also registers the following blueprints:
  - 'auth' for handling user registration and login.
  - 'main' for the core task management functionality.
  - 'api' for the RESTful API endpoints.

The application uses an SQLite database located in the 'instance' folder.
"""

from flask import Flask, redirect, url_for, flash
from .config import DevConfig
from .extensions import db, bcrypt, login_manager
import os
from .auth import routes as auth_routes
from .main import routes as main_routes
from .api import routes as api_routes
from .models import User


def create_app(config_object=DevConfig): # default to DevConfig
    """Application factory function."""
    app = Flask(__name__, instance_relative_config=True)

    # Configure the application from the DevConfig / ProdConfig class
    app.config.from_object(config_object)

    # Ensure the instance folder for database exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app) # Initialize SQLAlchemy database connection
    bcrypt.init_app(app) # Initialize Bcrypt for password hashing
    login_manager.init_app(app) # Initialize LoginManager for user session management

    # Configure LoginManager behavior
    login_manager.login_view = 'auth.login' # Redirect to 'auth.login' for @login_required

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) # Assuming user_id is the primary key and is an integer
    
    # Unauthorized handler to flash message and redirect to login
    @login_manager.unauthorized_handler
    def unauthorized():
        flash('You must be logged in to access this page.', 'warning')
        return redirect(url_for('auth.login'))

    # Register blueprints
    app.register_blueprint(auth_routes.auth_bp, url_prefix='/auth') # authentication routes
    app.register_blueprint(main_routes.main_bp, url_prefix='/') # task management routes
    app.register_blueprint(api_routes.api_bp, url_prefix='/api') # API routes

    return app