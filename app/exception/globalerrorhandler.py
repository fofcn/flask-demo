from flask import jsonify, render_template
import werkzeug
from . import globalexcept



@globalexcept.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@globalexcept.errorhandler(Exception)
def handle_exception(e):
    code = 500
    return jsonify(err=str(e)), code
    if isinstance(e, werkzeug.exceptions.HttpException):
        return e