
from flask import Blueprint, Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from . import config
from flask_swagger import swagger


db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(config.FlaskConfig)

    jwt = JWTManager(app)
   
    bootstrap = Bootstrap4(app)
    db.init_app(app=app)


    
    
    api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
    from . import auth
    api_v1.register_blueprint(auth.auth)
    from . import user
    api_v1.register_blueprint(user.user)
    from . import fs
    api_v1.register_blueprint(fs.file)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        from . import user
        return user.models.User.query.filter_by(id=identity).one_or_none()

    with app.app_context():
        db.create_all()

    @api_v1.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = 'v1.0.0'
        swag['info']['title'] = 'NAS'
        swag['info']['basePath'] = '/api/v1'
        swag['swagger'] = '2.0'
        return jsonify(swagger(app))
    
    from flask_swagger_ui import get_swaggerui_blueprint

    SWAGGER_URL="/swagger"
    API_URL="/api/v1/spec"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'NAS'
        }
    )
    # api_v1.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(swagger_ui_blueprint)
    app.register_blueprint(api_v1)
   

    return app
