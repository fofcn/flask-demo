
from flask import Blueprint
from .. import app

helloworld = Blueprint('helloworld', __name__, url_prefix='/helloworld')

from . import routes

app.register_blueprint(helloworld)