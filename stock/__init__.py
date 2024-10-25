from flask import Blueprint

bp = Blueprint('stock', __name__)

# Import routes here to register them with the blueprint
from . import routes
