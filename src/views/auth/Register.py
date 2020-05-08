from flask import request, make_response, jsonify
from flask.views import MethodView

from src import bcrypt, db
from src.models import User, BlacklistToken
from src.defs.types import account_types


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        number_of_types = len(account_types)
        # check if user already exists
        user = User.query.filter_by(username=post_data.get("username")).first()
        if not user:
            try:
                user = User(
                    username=post_data.get("username"),
                    password=post_data.get("password"),
                    account_type=int(post_data.get("account_type"))
                    if number_of_types != 0
                    else None,
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    "status": "success",
                    "message": "Successfully registered.",
                    "auth_token": auth_token.decode(),
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    "status": "fail",
                    "message": "Some error occurred. Please try again.",
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                "status": "fail",
                "message": "User already exists. Please Log in.",
            }
            return make_response(jsonify(responseObject)), 409
