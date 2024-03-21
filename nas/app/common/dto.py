
from flask import jsonify

def make_response(bizCode, msg, data=None):
    response_data = {
        'bizCode': bizCode,
        'msg': msg,
        'data': data
    }
    return jsonify(response_data)

def make_success_resp(bizCode, data):
    return make_response(bizCode, '', data), 200