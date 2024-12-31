import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.routes.chat import chat_bp, _model  # Assuming your module is named chat.py


# Create a dummy Flask app for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(chat_bp)
    return app


# Create a test client to make requests to the app
@pytest.fixture
def client(app):
    return app.test_client()


# Test cases
def test_chat_valid_request(client, monkeypatch):
    """Test the /chat endpoint with a valid JSON request."""

    # Mock the model's generate_content method
    mock_response = MagicMock()
    mock_response.text = "Test response from the model."
    monkeypatch.setattr(_model, "generate_content", lambda x: mock_response)

    # Send a POST request with a valid message
    response = client.post(
        "/chat", json={"message": "Hello, model!"}, content_type="application/json"
    )

    # Assert the response status code and content
    assert response.status_code == 200
    assert response.json == {"response": "Test response from the model."}


def test_chat_missing_message(client):
    """Test the /chat endpoint with a missing message in the request body."""

    # Send a POST request without a message
    response = client.post("/chat", json={}, content_type="application/json")

    # Assert the response status code and error message
    assert response.status_code == 400
    assert response.json == {"error": "Missing 'message' in request body"}


def test_chat_invalid_json(client):
    """Test the /chat endpoint with an invalid JSON request."""

    # Send a POST request with invalid JSON content
    response = client.post(
        "/chat", data="This is not JSON", content_type="application/json"
    )

    # Assert the response status code
    assert response.status_code == 400
    
    # Decode the response data to a string and check the error message
    error_message = response.data.decode()
    assert error_message == '{"error":"Request must be JSON"}\n'

def test_chat_model_error(client, monkeypatch):
    """Test the /chat endpoint when the model raises an exception."""

    # Mock the model's generate_content method to raise an exception
    monkeypatch.setattr(
        _model, "generate_content", MagicMock(side_effect=Exception("Model error"))
    )

    # Send a POST request with a valid message
    response = client.post(
        "/chat", json={"message": "Hello, model!"}, content_type="application/json"
    )

    # Assert the response status code and error message
    assert response.status_code == 500
    assert response.json == {"error": "An error occurred during processing."}