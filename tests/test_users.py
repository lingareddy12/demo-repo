"""Tests for registration, login, and the /users/me endpoint."""


def register_user(client, email="alice@example.com", password="supersecret1"):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": "Alice Example", "password": password},
    )


def login_user(client, email="alice@example.com", password="supersecret1"):
    return client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )


def test_register_and_login(client):
    response = register_user(client)
    assert response.status_code == 201
    assert response.json()["email"] == "alice@example.com"

    login_response = login_user(client)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_register_duplicate_email_fails(client):
    register_user(client)
    response = register_user(client)
    assert response.status_code == 409


def test_login_wrong_password_fails(client):
    register_user(client)
    response = login_user(client, password="wrong-password")
    assert response.status_code == 401


def test_read_current_user_requires_auth(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_read_current_user(client):
    register_user(client)
    token = login_user(client).json()["access_token"]

    response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"
