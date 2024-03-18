

from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy import select

from ..middleware.authmiddleware import require_authentication
from . import user_jwt
from .models import UserModel
from . import db
from .usercustomexcept import UserException


@user_jwt.route('/login', methods=["GET", "POST"])
def login():
    data = request.get_json()
    access_token = create_access_token(identity=data['username'])
    return {
        'user':'xiaosi',
        'nickname': 'xiaosi',
        'accessToken': access_token
    }

@user_jwt.route('/create', methods=['POST'])
def createUser():
    data = request.get_json()
    user = UserModel(
        username=data['username'],
        email=data['email']
    )
    try: 
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        raise UserException(e)

    return {
        'code': 0,
        'userId': user.id
    }, 200


@user_jwt.route('/<int:id>', methods=['GET'])
def user_detail(id):
    user = db.get_or_404(UserModel, id)
    return user


@user_jwt.route('/list/all', methods=['GET'])
def list_all_user():
    user_list = [user.to_dict() for user in db.session.scalars(select(UserModel).order_by(UserModel.id))]
    return {
        'code': 0, 
        'data': user_list
    }

@user_jwt.route('/<int:id>', methods=["DELETE"])
def delete_user():
    pass