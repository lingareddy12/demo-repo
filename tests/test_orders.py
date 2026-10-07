"""Tests for the order checkout flow."""
from app.models.user import User


def register_and_login(client, email, password="supersecret1"):
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": "Test User", "password": password},
    )
    login = client.post("/api/v1/auth/login", data={"username": email, "password": password})
    return login.json()["access_token"]


def make_admin_token(client, db_session, email="admin@example.com"):
    token = register_and_login(client, email)
    user = db_session.query(User).filter(User.email == email).first()
    user.is_superuser = True
    db_session.commit()
    # Re-login so any future token checks reflect the superuser flag freshly.
    return register_and_login(client, email)


def create_product(client, admin_token, stock=5, price=10.0):
    response = client.post(
        "/api/v1/products",
        json={"name": "Gadget", "price": price, "stock": stock},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    return response.json()["id"]


def test_place_order_reduces_stock(client, db_session):
    admin_token = make_admin_token(client, db_session)
    product_id = create_product(client, admin_token, stock=5)

    buyer_token = register_and_login(client, "buyer@example.com")
    response = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": product_id, "quantity": 2}]},
        headers={"Authorization": f"Bearer {buyer_token}"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    assert body["items"][0]["quantity"] == 2

    product_response = client.get(f"/api/v1/products/{product_id}")
    assert product_response.json()["stock"] == 3


def test_place_order_insufficient_stock(client, db_session):
    admin_token = make_admin_token(client, db_session)
    product_id = create_product(client, admin_token, stock=1)

    buyer_token = register_and_login(client, "buyer2@example.com")
    response = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": product_id, "quantity": 5}]},
        headers={"Authorization": f"Bearer {buyer_token}"},
    )
    assert response.status_code == 409


def test_cannot_view_others_order(client, db_session):
    admin_token = make_admin_token(client, db_session)
    product_id = create_product(client, admin_token, stock=5)

    buyer_token = register_and_login(client, "buyer3@example.com")
    order_id = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": product_id, "quantity": 1}]},
        headers={"Authorization": f"Bearer {buyer_token}"},
    ).json()["id"]

    other_token = register_and_login(client, "other@example.com")
    response = client.get(
        f"/api/v1/orders/{order_id}", headers={"Authorization": f"Bearer {other_token}"}
    )
    assert response.status_code == 403


def test_pay_order(client, db_session):
    admin_token = make_admin_token(client, db_session)
    product_id = create_product(client, admin_token, stock=5)

    buyer_token = register_and_login(client, "buyer4@example.com")
    order_id = client.post(
        "/api/v1/orders",
        json={"items": [{"product_id": product_id, "quantity": 1}]},
        headers={"Authorization": f"Bearer {buyer_token}"},
    ).json()["id"]

    response = client.post(
        f"/api/v1/orders/{order_id}/pay", headers={"Authorization": f"Bearer {buyer_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "paid"
