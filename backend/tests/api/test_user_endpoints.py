def test_create_user(client):
    response = client.post(
        "/users", json={"username": "newuser", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    assert "hashed_password" not in response.json()


def test_create_duplicate_user(client):
    client.post("/users", json={"username": "dupeuser", "password": "password123"})
    response = client.post(
        "/users", json={"username": "dupeuser", "password": "password123"}
    )
    assert response.status_code == 409


def test_delete_requires_auth(client, user_john):
    response = client.delete(f"/users/{user_john.username}")
    assert response.status_code == 401


def test_delete_user(auth_client, user_john):
    response = auth_client.delete(f"/users/{user_john.username}")
    assert response.status_code == 204
