"""
This file initializes the 'main' blueprint.
This blueprint handles the core application logic after a user is logged in.
"""
from flask import Blueprint

main_bp = Blueprint('main', __name__, template_folder='templates')

from . import routes