from flask import request, make_response, jsonify

from src.models import User


def login_required(function):
    def wrap(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    "status": "fail",
                    "message": "Bearer token malformed.",
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = None
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return function(*args, **kwargs)
            responseObject = {"status": "fail", "message": resp}
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                "status": "fail",
                "message": "Provide a valid auth token.",
            }
            return make_response(jsonify(responseObject)), 401

    wrap.__name__ = function.__name__
    return wrap
