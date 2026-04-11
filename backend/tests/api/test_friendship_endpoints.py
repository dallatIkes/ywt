def test_send_friend_request(auth_client, user_jane):
    response = auth_client.post(
        "/friendships/request", json={"addressee_id": user_jane.id}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pending"


def test_send_request_to_self(auth_client, user_john):
    response = auth_client.post(
        "/friendships/request", json={"addressee_id": user_john.id}
    )
    assert response.status_code == 403


def test_send_duplicate_request(auth_client, user_jane):
    auth_client.post("/friendships/request", json={"addressee_id": user_jane.id})
    response = auth_client.post(
        "/friendships/request", json={"addressee_id": user_jane.id}
    )
    assert response.status_code == 409


def test_accept_request(auth_client, auth_client_jane, user_jane):
    req = auth_client.post(
        "/friendships/request", json={"addressee_id": user_jane.id}
    ).json()
    response = auth_client_jane.patch(
        f"/friendships/{req['id']}/respond", json={"status": "accepted"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"


def test_decline_request(auth_client, auth_client_jane, user_jane):
    req = auth_client.post(
        "/friendships/request", json={"addressee_id": user_jane.id}
    ).json()
    response = auth_client_jane.patch(
        f"/friendships/{req['id']}/respond", json={"status": "declined"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "declined"


def test_wrong_user_cannot_respond(auth_client, user_jane):
    req = auth_client.post(
        "/friendships/request", json={"addressee_id": user_jane.id}
    ).json()
    response = auth_client.patch(
        f"/friendships/{req['id']}/respond", json={"status": "accepted"}
    )
    assert response.status_code == 403


def test_get_friends(auth_client, auth_client_jane, user_jane):
    req = auth_client.post(
        "/friendships/request", json={"addressee_id": user_jane.id}
    ).json()
    auth_client_jane.patch(
        f"/friendships/{req['id']}/respond", json={"status": "accepted"}
    )
    response = auth_client.get("/friendships/friends")
    assert response.status_code == 200
    assert any(f["username"] == "janeDoe" for f in response.json())


def test_get_pending(auth_client, auth_client_jane, user_jane):
    auth_client.post("/friendships/request", json={"addressee_id": user_jane.id})
    response = auth_client_jane.get("/friendships/pending")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_requires_auth(client, user_jane):
    response = client.post("/friendships/request", json={"addressee_id": user_jane.id})
    assert response.status_code == 401
