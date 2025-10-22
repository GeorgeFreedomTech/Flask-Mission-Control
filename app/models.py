"""
This module defines the database models for the application using SQLAlchemy.

- User: Represents a user with login credentials.
- Task: Represents a single to-do task associated with a user.

- The User model has a one-to-many relationship with the Task model.
- The User model inherits from UserMixin to integrate with Flask-Login 
  providing default implementations for user authentication methods like is_authenticated, is_active, is_anonymous, and get_id.
"""

from .extensions import db, bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin): # Multiple inheritance from db.Model and UserMixin
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True) # One-to-many relationship with Task

    def __repr__(self):
        return f"<User {self.email}>"

    def set_password(self, password):
        """Set password method to hash passwords using bcrypt"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check password method to verify passwords using bcrypt"""
        return bcrypt.check_password_hash(self.password_hash, password)
    

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    finished = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now()) # Timestamp of creation using server default
    due_date = db.Column(db.DateTime, nullable=False) # Due date for the task dd/mm/yyyy
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign key to User

    def __repr__(self):
        return f"<Task {self.name} - Finished: {self.finished}>"
    
    def to_dict(self):
        """Return a dictionary representation of the Task."""
        return {
            "id": self.id,
            "name": self.name,
            "finished": self.finished,
            "time_stamp": self.timestamp.isoformat() + 'Z', # ISO 8601 format for UTC
            "due_date": self.due_date.isoformat(),         # ISO 8601 format
            "user_id": self.user_id
        }