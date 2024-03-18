
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4

from app.config.config import FlaskConfig

app = Flask(__name__)
app.config.from_object(FlaskConfig)
jwt = JWTManager(app)
bootstrap = Bootstrap4(app)


db = SQLAlchemy(app)
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
engine = create_engine("postgresql://postgres:postgres@localhost:5432/supply_chain?client_encoding=UTF-8", echo=True)

Base = declarative_base()

# this is very very import to import your custom routes
# from routes.helloworld import routes
# from routes.pay import routes
# from routes.index import routes

# from app.exception import globalerrorhandler

# from middleware import loggermiddleware

from . import helloworld
from . import user
from . import exception

