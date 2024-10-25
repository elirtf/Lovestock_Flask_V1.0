from flask import Blueprint

auth = Blueprint('auth', __name__)

# Import routes here to register them with the blueprint
from . import routes
