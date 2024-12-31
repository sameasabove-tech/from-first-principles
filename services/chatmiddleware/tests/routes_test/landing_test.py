from typing import Any

import pytest
from flask import Flask
from flask import render_template

from src.routes.landing_routes import index_bp


# Create a dummy Flask app for testing
@pytest.fixture
def app():
    app = Flask(
        __name__, template_folder="../../src/templates"
    )  # Point to your templates
    app.register_blueprint(index_bp)
    return app


# Create a test client to make requests to the app
@pytest.fixture
def client(app: Flask):
    return app.test_client()


def test_index_route_renders_template(client: Any, app: Flask):
    """Test that the / route renders the index.html template."""

    # Simulate a request to the / route
    response = client.get("/")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains the expected content from index.html
    # You can check for specific elements or text in your template
    assert b"<!DOCTYPE html>" in response.data  # Check for doctype
    assert b"</html>" in response.data  # Check for html tag
    # Example: assert b"<h1>Welcome</h1>" in response.data (if your template has this)

    # You can also test the rendered template content more directly (less recommended)
    with app.app_context():
        rendered_template = render_template("index.html")
        assert response.data.decode() == rendered_template
