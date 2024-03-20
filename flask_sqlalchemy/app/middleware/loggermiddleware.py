
import time
from flask import Response, request
from . import middleware

class LoggerMiddleware:

    @staticmethod
    @middleware.before_reqeust
    def start_timer():
        request.start_time = time.time()


    @staticmethod
    @middleware.after_request
    def log_request():
        start_time = request.start_time
        duration = time.time() - start_time
        method = request.method
        url = request.path
        status = Response.status_code
        middleware.logger.info(f'{method} {url} {status} {duration * 1000} ms')
        return Response