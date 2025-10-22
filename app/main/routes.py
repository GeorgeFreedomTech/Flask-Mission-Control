"""
This module contains the main routes for the task management dashboard.
It handles displaying, creating, updating, and deleting tasks for the logged-in user.
"""
from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from . import main_bp
from flask_login import current_user
from ..models import Task
from ..extensions import db
from ..auth.forms import TaskForm


@main_bp.route('/')
def index():
    """Render the landing page of the application."""
    return render_template('main/index.html')

@main_bp.route('/about')
def about(): 
    """Render the about page of the application."""
    return render_template('main/about.html')

@main_bp.route('/dashboard') 
@login_required
def dashboard():
    """Render the dashboard page showing user's tasks."""
    tasks = current_user.tasks # get tasks from DB for the logged-in user
    form = TaskForm()  # Form for deleting tasks
    return render_template('main/dashboard.html', tasks=tasks, form=form)

@main_bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    """Handle adding a new task for the logged-in user."""
    form = TaskForm()

    if form.validate_on_submit():
        # Create a new task and add it to the database
        new_task = Task(name=form.name.data, due_date=form.due_date.data, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('main/add_task.html', form=form, submit_button_text='Add Task')

@main_bp.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    """Handle updating an existing task for the logged-in user."""
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('main.dashboard'))
    form = TaskForm(obj=task)  # Pre-fill form with existing task data
    
    if form.validate_on_submit():
        task.name = form.name.data
        task.due_date = form.due_date.data
        task.finished = form.finished.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('main/update_task.html', form=form, task=task, submit_button_text='Update Task')

@main_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """Handle deleting a task for the logged-in user."""
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('main.dashboard'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))