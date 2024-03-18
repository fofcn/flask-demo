
from flask import Blueprint
from flask_jwt_extended import jwt_required
from .. import app
from .. import db

from functools import wraps
from flask import Blueprint

class JWTBlueprint(Blueprint):
    def route(self, rule, **options):
        options['provide_automatic_options'] = False

        def decorator(f):
            f = jwt_required()(f)
            endpoint = options.pop("endpoint", f.__name__)
            
            def wrapper(*args, **kwargs):
                # 异常处理等其他逻辑
                return f(*args, **kwargs)

            self.add_url_rule(rule, endpoint, wrapper, **options)
            return wrapper

        return decorator

user_jwt = JWTBlueprint('user', __name__, url_prefix='/user')

from . import views
from . import userexception

app.register_blueprint(user_jwt)