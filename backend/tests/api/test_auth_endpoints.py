def test_login_returns_token(client, user_john):
    response = client.post(
        "/token", data={"username": "johnDoe", "password": "admin1234"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client, user_john):
    response = client.post(
        "/token", data={"username": "johnDoe", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post(
        "/token", data={"username": "nobody", "password": "admin1234"}
    )
    assert response.status_code == 401


def test_get_me(auth_client, user_john):
    response = auth_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["username"] == user_john.username
    assert "hashed_password" not in response.json()


def test_get_me_without_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401
