
from flask import Blueprint

from .. import app


middleware = Blueprint('middleware', __name__, )

app.register_blueprint(middleware)