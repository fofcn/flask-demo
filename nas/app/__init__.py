
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from . import config

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(config.FlaskConfig)

    jwt = JWTManager(app)
   
    bootstrap = Bootstrap4(app)
    db.init_app(app=app)

    from . import auth
    app.register_blueprint(auth.auth)
    from . import user
    app.register_blueprint(user.user)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return user.User.query.filter_by(id=identity).one_or_none()
    from . import fs

    with app.app_context():
        db.create_all()

    return app
