"""
This module defines custom command-line interface (CLI) commands for the application.
These commands are registered with Flask's CLI runner and can be invoked
using the `flask` command in the terminal (e.g., `flask init-db`).
"""

import click
from flask import current_app # to access app context if needed
from flask.cli import with_appcontext
from .extensions import db

@click.command('init-db') # cmd: flask init-db
@with_appcontext
def init_db_command():
    """Initialize the database."""
    
    db.create_all()
    click.echo('Initialized the database.')

def register_commands(app):
    """Register custom CLI commands with the Flask app."""
    app.cli.add_command(init_db_command)

