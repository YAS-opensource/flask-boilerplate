from flask import request, make_response, jsonify
from flask.views import MethodView

from src import bcrypt, db
from src.models import User, BlacklistToken


class UserAPI(MethodView):
    """
    User Resource
    """

    def get(self):
        # get the auth token
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
            auth_token = ""
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                responseObject = {
                    "status": "success",
                    "data": {
                        "user_id": user.id,
                        "username": user.username,
                        "registered_on": user.registered_on,
                    },
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {"status": "fail", "message": resp}
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                "status": "fail",
                "message": "Provide a valid auth token.",
            }
            return make_response(jsonify(responseObject)), 401
