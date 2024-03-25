
from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required

from . import dto


def jwt_required_ext(optional=False):

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return jwt_required(optional=optional)(fn)(*args, **kwargs)
            except Exception as e:
                return dto.make_response(1, 'Unauthorizaiton'), 401
        return wrapper
    return decorator