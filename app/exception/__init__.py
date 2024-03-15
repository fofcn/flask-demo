
from flask import Blueprint
from .. import app

globalexcept = Blueprint('globalexcept', __name__, )

app.register_blueprint(globalexcept)