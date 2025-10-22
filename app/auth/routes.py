"""
This module contains the routes for user authentication.
"""

from flask import render_template, redirect, url_for, flash
from . import auth_bp
from .forms import LoginForm, RegistrationForm
from ..extensions import db
from flask_login import login_user, logout_user, login_required
from ..models import User


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Route for user registration."""
    form = RegistrationForm()
    if form.validate_on_submit():
        # Handle registration logic
        # Check database if user exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('User with this email already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        # If not, create new user and add to database
        new_user = User(email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in and redirect to main.index
        login_user(new_user)
        flash('Registration successful!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Route for user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # create user session
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Route for user logout."""
    logout_user() # delete user session
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))