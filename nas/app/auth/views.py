
from flask import jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required
import jwt
from . import auth, models, dto
from .. import common

@auth.route('login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = models.User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return dto.make_auth_401()

    additional_claims = {"aud": "some_audience", "foo": "bar"}
    access_token = create_access_token(identity=user, additional_claims=additional_claims)
    return common.dto.make_success_resp(0, access_token)

@auth.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        full_name=current_user.full_name,
        username=current_user.username,
    )


