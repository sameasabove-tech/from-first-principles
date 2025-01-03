import pytest
from fastapi.testclient import TestClient

from src.main import create_app


@pytest.fixture
def client():
    """Create a TestClient instance for making requests to the FastAPI app."""
    app = create_app()
    return TestClient(app)


'''
Deprecated tests: see issue #14 (https://github.com/justmeloic/from-first-principles/issues/14)

def test_chat_endpoint_status_code(client: TestClient):
    """Test that the chat endpoint returns a 200 status code."""
    response = client.post("/api/v1/chat", json={"message": "Hello"})
    assert response.status_code == 200

def test_chat_endpoint_response(client: TestClient):
    """Test that the chat endpoint returns the expected response."""
    response = client.post("/api/v1/chat", json={"message": "Hello"})
    assert response.status_code == 200
    json_response = response.json()
    assert "response" in json_response
    assert isinstance(json_response["response"], str)
'''


def test_chat_endpoint_missing_message(client: TestClient):
    """Test that the chat endpoint returns a 422 status code for missing message."""
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422


def test_chat_endpoint_invalid_message(client: TestClient):
    """Test that the chat endpoint returns a 422 status code for invalid message."""
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422
