"""
This module defines the web forms for the authentication blueprint using Flask-WTF.

- RegistrationForm: For new user registration.
- LoginForm: For existing user login.
- TaskForm: For creating and updating tasks.
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo


# RegistrationForm - email, password, confirm password, submit
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# LoginForm - email, password, submit
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# TaskForm - title, due_date, submit
class TaskForm(FlaskForm):
    name = StringField('Task Name', validators=[DataRequired(), Length(max=150)])
    due_date = DateField('Due Date', validators=[DataRequired()], format='%Y-%m-%d')
    finished = BooleanField('Finished', default=False)
    submit = SubmitField('Submit')