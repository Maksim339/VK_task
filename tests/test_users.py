from uuid import uuid4


def test_create_user(client):
    project_id = uuid4()
    user_data = {
        "login": "test@example.com",
        "password": "password123",
        "project_id": str(project_id),
        "env": "dev",
        "domain": "regular"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["login"] == user_data["login"]
    assert "id" in response.json()


def test_get_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_acquire_and_release_lock(client):
    project_id = uuid4()
    user_data = {
        "login": "lock@example.com",
        "password": "password123",
        "project_id": str(project_id),
        "env": "dev",
        "domain": "regular"
    }
    user_response = client.post("/users/", json=user_data)
    user_id = user_response.json()["id"]

    lock_response = client.post(f"/users/{user_id}/lock")
    assert lock_response.status_code == 200
    assert lock_response.json()["is_locked"] is True

    unlock_response = client.post(f"/users/{user_id}/unlock")
    assert unlock_response.status_code == 200
    assert unlock_response.json()["is_locked"] is False
