
class BaseException(Exception):
    
    def __init__(self, msg, e) -> None:
        super().__init__(msg)
        self.e = e