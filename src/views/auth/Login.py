from flask import request, make_response, jsonify
from flask.views import MethodView

from src import bcrypt, db
from src.models import User, BlacklistToken


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(username=post_data.get("username")).first()
            if user and bcrypt.check_password_hash(
                user.password, post_data.get("password")
            ):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        "status": "success",
                        "message": "Successfully logged in.",
                        "auth_token": auth_token.decode(),
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {"status": "fail", "message": "User does not exist."}
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {"status": "fail", "message": "Try again"}
            return make_response(jsonify(responseObject)), 500
