from ..common import dto

def make_auth_401():
    return dto.make_response(0, "username or password is incorrect", None), 401

