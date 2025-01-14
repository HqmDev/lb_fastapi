import json

import pytest

from app.api import crud


def test_create_restaurant(test_app, monkeypatch):
    test_request_payload = {"title": "something", "description": "something else"}
    test_response_payload = {"id": 1, "title": "something", "description": "something else"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/restaurants/", content=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_restaurant_invalid_json(test_app):
    response = test_app.post("/restaurants/", content=json.dumps({"title": "something"}))
    assert response.status_code == 422


def test_read_restaurant(test_app, monkeypatch):
    test_data = {"id": 1, "title": "something", "description": "something else"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/restaurants/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_restaurant_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/restaurants/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found"

    response = test_app.get("/restaurants/0")
    assert response.status_code == 422


def test_read_all_restaurants(test_app, monkeypatch):
    test_data = [
        {"title": "something", "description": "something else", "id": 1},
        {"title": "someone", "description": "someone else", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/restaurants/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_restaurant(test_app, monkeypatch):
    test_update_data = {"title": "someone", "description": "someone else", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/restaurants/1/", content=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
    ],
)
def test_update_restaurant_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/restaurants/{id}/", content=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_restaurant(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/restaurants/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_restaurant_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/restaurants/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found"