
import werkzeug

import app


class InsufficientStorage(werkzeug.exceptions.HttpException):
    code = 507
    description = 'Not enough storage space.'

app.register_error_handler(InsufficientStorage, 507)