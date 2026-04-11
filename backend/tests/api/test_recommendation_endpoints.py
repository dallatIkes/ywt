def test_send_reco(auth_client, user_jane):
    response = auth_client.post(
        "/recommendations/send",
        json={
            "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "description": "Watch this!",
            "to_user_id": user_jane.id,
        },
    )
    assert response.status_code == 201
    assert "embed" in response.json()["link"]


def test_send_reco_to_self(auth_client, user_john):
    response = auth_client.post(
        "/recommendations/send",
        json={
            "link": "https://youtu.be/dQw4w9WgXcQ",
            "description": "Watch this!",
            "to_user_id": user_john.id,
        },
    )
    assert response.status_code == 403


def test_send_reco_requires_auth(client, user_jane):
    response = client.post(
        "/recommendations/send",
        json={
            "link": "https://youtu.be/dQw4w9WgXcQ",
            "description": "Watch this!",
            "to_user_id": user_jane.id,
        },
    )
    assert response.status_code == 401


def test_get_sent(auth_client, user_jane):
    auth_client.post(
        "/recommendations/send",
        json={
            "link": "https://youtu.be/dQw4w9WgXcQ",
            "description": "Watch this!",
            "to_user_id": user_jane.id,
        },
    )
    response = auth_client.get("/recommendations/sent")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_received(auth_client, auth_client_jane, user_jane):
    auth_client.post(
        "/recommendations/send",
        json={
            "link": "https://youtu.be/dQw4w9WgXcQ",
            "description": "Watch this!",
            "to_user_id": user_jane.id,
        },
    )
    response = auth_client_jane.get("/recommendations/received")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_rate_reco(auth_client, auth_client_jane, user_jane):
    reco = auth_client.post(
        "/recommendations/send",
        json={
            "link": "https://youtu.be/dQw4w9WgXcQ",
            "description": "Watch this!",
            "to_user_id": user_jane.id,
        },
    ).json()
    response = auth_client_jane.patch(
        f"/recommendations/{reco['id']}/rating", json={"rating": 4}
    )
    assert response.status_code == 200
    assert response.json()["rating"] == 4


def test_rate_reco_wrong_user(auth_client, user_jane):
    reco = auth_client.post(
        "/recommendations/send",
        json={
            "link": "https://youtu.be/dQw4w9WgXcQ",
            "description": "Watch this!",
            "to_user_id": user_jane.id,
        },
    ).json()
    response = auth_client.patch(
        f"/recommendations/{reco['id']}/rating", json={"rating": 4}
    )
    assert response.status_code == 403
