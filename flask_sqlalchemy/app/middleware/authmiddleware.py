
import os

from flask import request
import jwt

class AuthException(Exception):

    def __init__(self, msg, http_status_code) -> None:
        super().__init__(msg)
        self.http_status_code = http_status_code

class AuthMiddleware:

    @staticmethod
    def is_valid_token(token):
        secret = os.getenv('SECRET')
        try:
            return jwt.decode(token, secret, algorithms=["HS256"])
        except Exception as e:
            print(str(e))

    def authenticate(self):
        auth_token = request.headers.get('Authorization')

        if not auth_token or not self.is_valid_token(auth_token):
            raise AuthException('Unauthorized', 401)


def require_authentication(func):
    def wrapper(*args, **kwargs):
        AuthMiddleware().authenticate()
        return func(*args, **kwargs)

    return wrapper