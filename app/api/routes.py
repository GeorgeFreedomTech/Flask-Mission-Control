"""
This module defines API routes for managing tasks in a Flask application.
It allows authenticated users to retrieve and create tasks via JSON requests.
"""

from flask import jsonify, request
from flask_login import login_required, current_user
from . import api_bp
from ..models import Task, db
from datetime import datetime

@api_bp.route('/tasks', methods=['GET', 'POST'])
@login_required
def api_tasks():
    """Handles GET and POST requests for tasks."""
    if request.method == 'GET':
        tasks = current_user.tasks 
        response = [task.to_dict() for task in tasks]
        return jsonify(response), 200
    
    elif request.method == 'POST':
        data = request.json
        if not data or 'name' not in data or 'due_date' not in data:
            return jsonify({"error": "Missing required fields: name and due_date"}), 400
        
        # **Parse the incoming date string (assuming ISO 8601)**
        try: 
            due_date_obj = datetime.fromisoformat(data['due_date'])
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO 8601 (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"}), 400
        
        new_task = Task(name=data['name'], due_date=due_date_obj, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201