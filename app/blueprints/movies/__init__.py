from flask import Blueprint
movies_bp = Blueprint("movies", __name__)
from . import routes
