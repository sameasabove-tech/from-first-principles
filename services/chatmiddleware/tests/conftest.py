import os
import sys
import pytest

from src.appfactory import create_middleware_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_middleware_app()
    app.config.update({
        "TESTING": True,  # Enable testing mode
        "DEBUG": False,
    })
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()