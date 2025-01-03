"""
Chat router module.

This module defines the API router for handling chat-related requests.
It uses a pre-initialized Gemini model to generate responses to user messages.
"""

import os

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field

from models.chat_model import get_model  # Assuming your model has a GeminiModel class


# Load the Gemini API key from environment variables
try:
    _GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
except KeyError as e:
    raise ValueError("GEMINI_API_KEY environment variable must be set.") from e

# Initialize the AI model outside the request context for efficiency
_model = get_model(api_key=_GEMINI_API_KEY)
if _model is None:
    raise RuntimeError(
        "Failed to initialize the Gemini model. Ensure API Key and model availability."
    )


# Define router
router = APIRouter(
    tags=["chat"],
)


# Pydantic model for request body
class ChatRequest(BaseModel):
    """
    Represents a chat request with a single message field.

    Attributes:
        message: The message sent by the user.
    """

    message: str = Field(
        ...,
        description="The message content for the chat interaction.",
        min_length=1,
        json_schema_extra={"example": "Hello, how are you?"},
    )


# Pydantic model for response body
class ChatResponse(BaseModel):
    """
    Represents the response from the chat endpoint.

    Attributes:
        response: The generated response from the model.
    """

    response: str = Field(
        ..., description="The generated response from the chat model."
    )


@router.post("/chat", response_model=ChatResponse)
async def handle_chat(chat_request: ChatRequest) -> ChatResponse:
    """
    Handles chat requests by generating responses using a Gemini model.

    Args:
        chat_request: The incoming chat request containing the user's message.

    Raises:
        HTTPException: If an error occurs during model processing.

    Returns:
        ChatResponse: The generated response from the model.
    """
    try:
        response = _model.generate_content(chat_request.message)
        return ChatResponse(response=response.text)

    except Exception as e:  # Catch potential model errors
        print(f"Error during model processing: {e}")  # Log the error for debugging
        raise HTTPException(
            status_code=500, detail="An error occurred during processing."
        ) from e
