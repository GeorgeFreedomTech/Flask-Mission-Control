"""
Web Server Gateway Interface (WSGI) entry point.

This module is the main entry point for the Gunicorn or other WSGI servers.
It finds and runs the application factory 'create_app' from our main package.
Its sole purpose is to create and run the app.
"""
from app import create_app
from app import commands

app = create_app()

# Register custom CLI commands
commands.register_commands(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0') # Run the app on all available interfaces for local testing