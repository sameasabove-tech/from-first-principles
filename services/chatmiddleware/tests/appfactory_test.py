import os
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from flask import Flask

from src.appfactory import create_middleware_app


# Assuming your app factory function is in src.appfactory


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("TEST_ENV_VAR", "test_value")


def apply_patches_after_app_creation(app):
    """Applies patches after the app has been created."""
    with patch(
        "src.routes.chat.chat_bp", new_callable=MagicMock
    ) as mock_chat_bp, patch(
        "src.routes.landing.index_bp", new_callable=MagicMock
    ) as mock_index_bp:
        # Now, we re-register the blueprints with our mocks.
        app.register_blueprint(mock_chat_bp)
        app.register_blueprint(mock_index_bp)


def is_cors_enabled(app):
    """Checks if CORS is enabled in the app's after_request functions."""
    for fns in app.after_request_funcs.values():
        for fn in fns:
            if getattr(fn, "__name__", None) == "cors_after_request":
                return True
    return False


def test_create_middleware_app_success(mock_env):
    """Test successful creation of the Flask app."""
    app = create_middleware_app()
    apply_patches_after_app_creation(app)

    assert isinstance(app, Flask)
    # Check if CORS is enabled using the new function
    assert is_cors_enabled(app)

    # Load environment variables from the mocked environment
    for key, value in os.environ.items():
        app.config[key] = value

    # Check that the environment variable was set
    assert app.config["TEST_ENV_VAR"] == "test_value"


def test_create_middleware_app_no_env_file(monkeypatch):
    """Test that RuntimeError is raised when .env file is missing."""

    # Mock load_dotenv to raise FileNotFoundError
    monkeypatch.setattr(
        "src.appfactory.load_dotenv", MagicMock(side_effect=FileNotFoundError)
    )

    with pytest.raises(RuntimeError) as excinfo:
        create_middleware_app()

    assert "'.env' file not found" in str(excinfo.value)
