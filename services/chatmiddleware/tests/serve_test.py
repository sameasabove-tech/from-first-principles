import pytest
from unittest.mock import patch, MagicMock
from src.serve import app, run_server  # Import app and the new function

@patch("src.serve.app.run")  # Mock app.run
def test_serve_starts_app(mock_run):
    """Test that app.run is called with the correct arguments."""

    run_server()  # Call the function to start the server

    mock_run.assert_called_once_with(debug=True, port=8080)