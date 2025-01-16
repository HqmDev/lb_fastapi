import pytest
import json

import pytest
from app.api import crud


@pytest.mark.asyncio
async def test_create_user(test_app, monkeypatch):
    payload = {"username": "testuser", "email": "testuser@example.com", "password": "password"}

    async def mock_create_user(payload):
        return {**payload, "id": 1, "is_active": True}

    monkeypatch.setattr("app.api.crud.create_user", mock_create_user)

    response = test_app.post("/users/", json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]


@pytest.mark.asyncio
async def test_get_user(test_app, monkeypatch):
    user_data = {"id": 1, "username": "testuser", "email": "testuser@example.com", "is_active": True}

    async def mock_get_user_by_id(user_id):
        return user_data

    monkeypatch.setattr("app.api.crud.get_user_by_id", mock_get_user_by_id)

    response = test_app.get("/users/1/")
    assert response.status_code == 200
    assert response.json() == user_data