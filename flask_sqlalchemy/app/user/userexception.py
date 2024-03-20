from flask import jsonify

from .usercustomexcept import UserException
from . import user_jwt

@user_jwt.errorhandler(UserException)
def handle_exception(e):
    code = 500
    print(e.e)
    return jsonify(err=str(e), msg='internal server error', bizCode='10001'), code