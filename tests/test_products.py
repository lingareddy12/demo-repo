"""Tests for the product catalog endpoints."""
from app.models.user import User


def make_admin_token(client, db_session, email="admin@example.com"):
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": "Admin User", "password": "supersecret1"},
    )
    user = db_session.query(User).filter(User.email == email).first()
    user.is_superuser = True
    db_session.commit()

    login = client.post(
        "/api/v1/auth/login", data={"username": email, "password": "supersecret1"}
    )
    return login.json()["access_token"]


def test_list_products_empty(client):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert response.json() == []


def test_non_admin_cannot_create_product(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "bob@example.com", "full_name": "Bob", "password": "supersecret1"},
    )
    token = client.post(
        "/api/v1/auth/login", data={"username": "bob@example.com", "password": "supersecret1"}
    ).json()["access_token"]

    response = client.post(
        "/api/v1/products",
        json={"name": "Widget", "price": 9.99, "stock": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_admin_can_create_and_fetch_product(client, db_session):
    token = make_admin_token(client, db_session)

    create_response = client.post(
        "/api/v1/products",
        json={"name": "Widget", "description": "A useful widget", "price": 9.99, "stock": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    get_response = client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Widget"


def test_get_missing_product_returns_404(client):
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404
