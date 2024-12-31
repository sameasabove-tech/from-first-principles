import os
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from dotenv import load_dotenv

from src.models.chat_model import get_model


# Load environment variables for testing if a .env file exists
load_dotenv()

# Use a test API key or mock the API key for testing
TEST_API_KEY = os.getenv("TEST_GEMINI_API_KEY", "mock_api_key")


def test_get_model_success():
    """Test successful model initialization with valid parameters."""
    mock_generative_model = MagicMock()

    with patch("src.models.chat_model.genai.configure") as mock_configure, patch(
        "src.models.chat_model.genai.GenerativeModel"
    ) as mock_gen_model:
        mock_gen_model.return_value = mock_generative_model

        model = get_model(TEST_API_KEY)

        mock_configure.assert_called_once_with(api_key=TEST_API_KEY)
        mock_gen_model.assert_called_once_with("gemini-1.5-flash")
        assert model == mock_generative_model


def test_get_model_with_system_prompt():
    """Test model initialization with a system prompt."""
    mock_generative_model = MagicMock()
    system_prompt = "You are a helpful assistant."

    with patch("src.models.chat_model.genai.configure"), patch(
        "src.models.chat_model.genai.GenerativeModel"
    ) as mock_gen_model:
        mock_gen_model.return_value = mock_generative_model

        model = get_model(TEST_API_KEY, system_prompt=system_prompt)

        mock_gen_model.assert_called_once_with("gemini-1.5-flash")
        # You might need to adjust this based on how generation_config is handled internally
        assert model == mock_generative_model


def test_get_model_invalid_model_name():
    """Test that an exception is raised for an invalid model name."""
    with patch("src.models.chat_model.genai.configure"), patch(
        "src.models.chat_model.genai.GenerativeModel"
    ) as mock_gen_model:
        mock_gen_model.side_effect = Exception("Invalid model name")

        with pytest.raises(Exception) as excinfo:
            get_model(TEST_API_KEY, model_name="invalid-model")

        assert "Invalid model name" in str(excinfo.value)


def test_get_model_configuration_failure():
    """Test that an exception is raised if genai.configure fails."""
    with patch("src.models.chat_model.genai.configure") as mock_configure:
        mock_configure.side_effect = Exception("API key configuration failed")

        with pytest.raises(Exception) as excinfo:
            get_model("invalid_api_key")  # Assuming this key would cause a config error

        assert "API key configuration failed" in str(excinfo.value)


def test_get_model_generate_content_success():
    """Test the generate_content method of the returned model."""
    mock_response = MagicMock()
    mock_response.text = "This is a test response."

    with patch("src.models.chat_model.genai.configure"), patch(
        "src.models.chat_model.genai.GenerativeModel"
    ) as mock_gen_model:
        mock_model = MagicMock()
        mock_gen_model.return_value = mock_model
        mock_model.generate_content.return_value = mock_response

        model = get_model(TEST_API_KEY)
        model.start_chat()
        response = model.generate_content("Test prompt")

        mock_model.generate_content.assert_called_once_with("Test prompt")
        assert response.text == "This is a test response."
