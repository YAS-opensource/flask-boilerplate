import os
import time
import json
import unittest

from src import db
from src.models import User, BlacklistToken
from src.tests.base import BaseTesting
from src.defs.types import account_types

is_type = True if len(account_types) > 0 else False

users = [
    ("user1", "user1", int(account_types["type1"]) if is_type else None),
    ("user2", "user2", int(account_types["type2"]) if is_type else None),
]


def base_register(self, data):
    return self.client.post(
        "/auth/register", data=json.dumps(data), content_type="application/json"
    )


def base_login(self, data):
    return self.client.post(
        "/auth/login", data=json.dumps(data), content_type="application/json"
    )


def base_auth_check(
    self, response, status, status_code, success_msg=None, is_auth_token=True
):
    data = json.loads(response.data.decode())
    self.assertTrue(data["status"] == status)
    if success_msg:
        self.assertTrue(data["message"] == success_msg)
    if is_auth_token:
        self.assertTrue(data["auth_token"])
    self.assertTrue(response.content_type == "application/json")
    self.assertEqual(response.status_code, status_code)


class TestAuthBluePrint(BaseTesting):
    """ Tests for auth """

    def test_registration(self):
        """ User registration test """
        with self.client:
            for user in users:
                response = base_register(
                    self,
                    {
                        "username": user[0],
                        "password": user[1],
                        "account_type": user[2],
                    },
                )
                base_auth_check(
                    self, response, "success", 201, "Successfully registered.",
                )

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        for user in users:
            dummy_user = User(username=user[0], password=user[1], account_type=user[2])
            db.session.add(dummy_user)
        db.session.commit()
        with self.client:
            for user in users:
                response = base_register(
                    self,
                    {"username": user[0], "password": user[1], "account_type": user[2]},
                )
                base_auth_check(
                    self,
                    response,
                    "fail",
                    409,
                    "User already exists. Please Log in.",
                    False,
                )

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        for user in users:
            dummy_user = User(username=user[0], password=user[1], account_type=user[2])
            db.session.add(dummy_user)
        db.session.commit()
        with self.client:
            for user in users:
                response = base_login(self, {"username": user[0], "password": user[1]})
                base_auth_check(
                    self, response, "success", 200, "Successfully logged in."
                )

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            for user in users:
                response = base_login(self, {"username": user[0], "password": user[1]})
                base_auth_check(
                    self, response, "fail", 404, "User does not exist.", False
                )

    def test_user_status(self):
        """ Test for user status """
        with self.client:
            for user in users:
                resp_register = base_register(
                    self,
                    {
                        "username": user[0],
                        "password": user[1],
                        "account_type": user[2],
                    },
                )
                response = self.client.get(
                    "/auth/status",
                    headers={
                        "Authorization": "Bearer "
                        + json.loads(resp_register.data.decode())["auth_token"]
                    },
                )
                data = json.loads(response.data.decode())
                self.assertTrue(data["data"] is not None)
                self.assertTrue(data["data"]["username"] == user[0])
                base_auth_check(self, response, "success", 200, None, False)

    def test_user_status_malformed_bearer_token(self):
        """ Test for user status with malformed bearer token"""
        with self.client:
            for user in users:
                resp_register = base_register(
                    self,
                    {
                        "username": user[0],
                        "password": user[1],
                        "account_type": user[2],
                    },
                )
                response = self.client.get(
                    "/auth/status",
                    headers={
                        "Authorization": "Bearer"
                        + json.loads(resp_register.data.decode())["auth_token"]
                    },
                )
                base_auth_check(
                    self, response, "fail", 401, "Bearer token malformed.", False
                )

    def test_valid_logout(self):
        """ Testing logout before token expires """
        with self.client:
            for user in users:
                resp_register = base_register(
                    self,
                    {
                        "username": user[0],
                        "password": user[1],
                        "account_type": user[2],
                    },
                )
                response = self.client.post(
                    "/auth/logout",
                    headers={
                        "Authorization": "Bearer "
                        + json.loads(resp_register.data.decode())["auth_token"]
                    },
                )
                base_auth_check(
                    self, response, "success", 200, "Successfully logged out.", False
                )

    def test_balcklisted_token_logout(self):
        """ Testing logout before token expires """
        with self.client:
            for user in users:
                resp_register = base_register(
                    self,
                    {
                        "username": user[0],
                        "password": user[1],
                        "account_type": user[2],
                    },
                )
                response = self.client.post(
                    "/auth/logout",
                    headers={
                        "Authorization": "Bearer "
                        + json.loads(resp_register.data.decode())["auth_token"]
                    },
                )
                response = self.client.post(
                    "/auth/logout",
                    headers={
                        "Authorization": "Bearer "
                        + json.loads(resp_register.data.decode())["auth_token"]
                    },
                )
                base_auth_check(self, response, "fail", 401, is_auth_token=False)
