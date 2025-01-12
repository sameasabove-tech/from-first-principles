import pytest
from fastapi.testclient import TestClient
from main import create_app

app = create_app()
client = TestClient(app)

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the FromFirstPrincipals Web Tracker API",
        "timestamp": response.json()["timestamp"]
    }

def test_track_hit():
    response = client.post("/track", json={
        "session_id": "test_session",
        "event_type": "page_load",
        "page": "test_page"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Event 'page_load' recorded!"