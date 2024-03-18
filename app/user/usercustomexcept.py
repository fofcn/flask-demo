
from ..exception.baseexception import BaseException

class UserException(BaseException):
    
    def __init__(self, e) -> None:
        super().__init__('user cannot create', e)