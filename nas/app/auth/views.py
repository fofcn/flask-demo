
import bcrypt
from flask import jsonify, request
from flask_jwt_extended import create_access_token, current_user, jwt_required
import jwt
from . import auth, models, dto
from .. import common

@auth.route('login', methods=['POST'])
def login():
    """
    login with username and password
    ---
    tasg:
      - Auth
    consumes:
      - application/json
    
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: 
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successfully
      schema:
        type: object
        properties:
        bizCode: 
          type: integer
          description: Auth should return 0
        msg:
          type: string
          description: empty string when success, error reason otherwise
        data: 
          type: string
          description: only access token returned when success

    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = models.User.query.filter_by(username=username).one_or_none()
    if not user:
        return dto.make_auth_401()
    
    input_pwd = password.encode('utf-8')
    hashed_pwd = user.password.encode('utf-8')
    if not bcrypt.checkpw(input_pwd, hashed_pwd):
        return dto.make_auth_401()

    additional_claims = {"aud": "some_audience", "foo": "bar"}
    access_token = create_access_token(identity=user, additional_claims=additional_claims)
    return common.dto.make_success_resp(0, access_token)

@auth.route("/info", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        full_name=current_user.full_name,
        username=current_user.username,
    )


