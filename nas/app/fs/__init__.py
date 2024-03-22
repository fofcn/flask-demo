from flask import Blueprint

file = Blueprint('file', __name__, url_prefix='/file')

from . import views