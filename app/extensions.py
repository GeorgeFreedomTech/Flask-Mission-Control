"""
This module initializes Flask extensions to avoid circular import issues.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy() # SQLAlchemy instance for database connection
bcrypt = Bcrypt() # Bcrypt instance for password hashing
login_manager = LoginManager() # LoginManager instance for user session management
