from flask import request, make_response, jsonify
from flask.views import MethodView

from src import bcrypt, db
from src.models import User, BlacklistToken


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    def post(self):
        # get auth token
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
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    responseObject = {
                        "status": "success",
                        "message": "Successfully logged out.",
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {"status": "fail", "message": e}
                    return make_response(jsonify(responseObject)), 500
            else:
                responseObject = {"status": "fail", "message": resp}
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                "status": "fail",
                "message": "Provide a valid auth token.",
            }
            return make_response(jsonify(responseObject)), 403
