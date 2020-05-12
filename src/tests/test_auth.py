import json

from src.defs.types import account_types

is_type = True if len(account_types) > 0 else False

users = [
    ("user1", "user1", int(account_types["type1"]) if is_type else None),
    ("user2", "user2", int(account_types["type2"]) if is_type else None),
]
non_registered_users = [
    ("user3", "user3", int(account_types["type1"]) if is_type else None),
    ("user4", "user4", int(account_types["type2"]) if is_type else None),
]
resp_register = {}


def base_register(client, data):
    return client.post(
        "/auth/register", data=json.dumps(data), content_type="application/json"
    )


def base_login(client, data):
    return client.post(
        "/auth/login", data=json.dumps(data), content_type="application/json"
    )


def base_auth_check(
    response, status, status_code, success_msg=None, is_auth_token=True
):
    data = json.loads(response.data.decode())
    assert data["status"] == status
    if success_msg:
        assert data["message"] == success_msg
    if is_auth_token:
        assert data["auth_token"]
    assert response.content_type == "application/json"
    assert response.status_code == status_code


def test_registration(client, database):
    """User registration test."""

    for user in users:
        username = user[0]
        password = user[1]
        account_type = user[2]

        response = base_register(
            client,
            {"username": username, "password": password, "account_type": account_type,},
        )

        # set response of register to global var for later usage
        global resp_register
        resp_register[username] = response

        base_auth_check(
            response, "success", 201, "Successfully registered.",
        )


def test_registered_with_already_registered_user(client, database):
    """Test registration with already registered email."""

    for user in users:
        username = user[0]
        password = user[1]
        account_type = user[2]

        response = base_register(
            client,
            {"username": username, "password": password, "account_type": account_type},
        )
        base_auth_check(
            response, "fail", 409, "User already exists. Please Log in.", False,
        )


def test_registered_user_login(client, database):
    """Test for login of registered-user login."""

    for user in users:
        username = user[0]
        password = user[1]

        response = base_login(client, {"username": username, "password": password})
        base_auth_check(response, "success", 200, "Successfully logged in.")


def test_non_registered_user_login(client, database):
    """Test for login of non-registered user."""

    for user in non_registered_users:
        username = user[0]
        password = user[1]

        response = base_login(client, {"username": username, "password": password})
        base_auth_check(response, "fail", 404, "User does not exist.", False)


def test_user_status(client):
    """Test for user status."""

    for user in users:
        username = user[0]
        user_data = resp_register[username].data

        response = client.get(
            "/auth/status",
            headers={
                "Authorization": "Bearer "
                + json.loads(user_data.decode())["auth_token"]
            },
        )

        data = json.loads(response.data.decode())
        assert data["data"] is not None
        assert data["data"]["username"] == username
        base_auth_check(response, "success", 200, None, False)


def test_user_status_malformed_bearer_token(client):
    """Test for user status with malformed bearer token."""
    for user in users:
        username = user[0]
        user_data = resp_register[username].data

        response = client.get(
            "/auth/status",
            headers={
                "Authorization": "Bearrr" + json.loads(user_data.decode())["auth_token"]
            },
        )
        base_auth_check(response, "fail", 401, "Bearer token malformed.", False)


def test_valid_logout(client):
    """Testing logout before token expires."""

    for user in users:
        username = user[0]
        user_data = resp_register[username].data

        response = client.post(
            "/auth/logout",
            headers={
                "Authorization": "Bearer "
                + json.loads(user_data.decode())["auth_token"]
            },
        )
        base_auth_check(
            response, "success", 200, "Successfully logged out.", False,
        )


def test_balcklisted_token_logout(client):
    """Testing blaclisted token logout before token expires."""

    for user in users:
        username = user[0]
        user_data = resp_register[username].data

        response = client.post(
            "/auth/logout",
            headers={
                "Authorization": "Bearer "
                + json.loads(user_data.decode())["auth_token"]
            },
        )
        base_auth_check(response, "fail", 401, is_auth_token=False)
