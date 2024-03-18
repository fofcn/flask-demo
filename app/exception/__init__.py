
from flask import Blueprint
from .. import app

globalexcept = Blueprint('globalexcept', __name__, )

from . import globalerrorhandler

app.register_blueprint(globalexcept)
