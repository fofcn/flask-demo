import bcrypt
from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from . import models, user
from .. import db
from .. import common


@user.route('/register', methods=['POST'])
def createUser():
    pwd = request.json.get('password')
    hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

    try:
        user = models.User(username=request.json.get('username'),
                            password=hashed_pwd.decode(),
                            email=request.json.get('email'),
                            full_name=request.json.get('full_name'))
        db.session.add(user)
        db.session.commit()
    
    except IntegrityError as e:
        db.session.rollback()
        return common.dto.make_response(0, 'username is incorrect', None), 500
    except Exception as e:
        db.session.rollback()
        return common.dto.make_response(0, str(e), None), 500
    return common.dto.make_success_resp(0, None)
    