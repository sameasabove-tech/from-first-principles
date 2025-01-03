"""
Chat router module.

This module defines the API router for handling chat-related requests.
It uses a pre-initialized Gemini model to generate responses to user messages.
"""

import os
import uuid

import redis
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field

from models.chat_model import get_model  # Assuming your model has a GeminiModel class


# Load environment variables
try:
    _GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    _REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")  # Default to localhost
    _REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))  # Default to 6379
    _REDIS_DB = int(os.environ.get("REDIS_DB", 0))  # Default to 0
except KeyError as e:
    raise ValueError(
        "Environment variables (GEMINI_API_KEY, REDIS_HOST, REDIS_PORT, REDIS_DB) must be set."
    ) from e


# Initialize the AI model outside the request context for efficiency
_model = get_model(api_key=_GEMINI_API_KEY)
if _model is None:
    raise RuntimeError(
        "Failed to initialize the Gemini model. Ensure API Key and model availability."
    )


# Redis client
def get_redis_client():
    """
    Dependency to get a Redis client.
    """
    try:
        r = redis.StrictRedis(
            host=_REDIS_HOST, port=_REDIS_PORT, db=_REDIS_DB, decode_responses=True
        )
        yield r
    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to connect to Redis."
        ) from e


# Define router
router = APIRouter(
    tags=["chat"],
)


# Pydantic model for request body
class ChatRequest(BaseModel):
    """
    Represents a chat request with a message field and an optional conversation ID.

    Attributes:
        message: The message sent by the user.
        conversation_id: An optional unique ID to track the conversation.
    """

    message: str = Field(
        ...,
        description="The message content for the chat interaction.",
        min_length=1,
        json_schema_extra={"example": "Hello, how are you?"},
    )
    conversation_id: str = Field(
        None,
        description="Unique identifier for the conversation. If not provided, a new conversation is started.",
        json_schema_extra={"example": "conv-1234-abcd-5678-efgh"},
    )


# Pydantic model for response body
class ChatResponse(BaseModel):
    """
    Represents the response from the chat endpoint.

    Attributes:
        response: The generated response from the model.
        conversation_id: The unique ID of the conversation.
    """

    response: str = Field(
        ..., description="The generated response from the chat model."
    )
    conversation_id: str = Field(
        ..., description="Unique identifier for the conversation."
    )


@router.post("/chat", response_model=ChatResponse)
async def handle_chat(
    chat_request: ChatRequest,
    redis_client: redis.StrictRedis = Depends(get_redis_client),
) -> ChatResponse:
    """
    Handles chat requests by generating responses using a Gemini model and maintains conversation history.

    Args:
        chat_request: The incoming chat request containing the user's message and optional conversation ID.
        redis_client: Redis client instance (dependency injected).

    Raises:
        HTTPException: If an error occurs during model processing or Redis interaction.

    Returns:
        ChatResponse: The generated response from the model and the conversation ID.
    """
    try:
        # Get or create conversation ID
        conversation_id = chat_request.conversation_id or str(uuid.uuid4())

        # Retrieve conversation history from Redis
        history = redis_client.lrange(conversation_id, 0, -1)
        history = [
            {"role": "user" if i % 2 == 0 else "model", "parts": [msg]}
            for i, msg in enumerate(history)
        ]

        # Prepare the full prompt (history + new message)
        messages = history + [{"role": "user", "parts": [chat_request.message]}]

        # Generate response using the model
        response = _model.generate_content(messages)

        # Add user message and model response to Redis
        redis_client.rpush(conversation_id, chat_request.message, response.text)

        return ChatResponse(response=response.text, conversation_id=conversation_id)

    except Exception as e:
        print(f"Error during model processing or Redis interaction: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred during processing."
        ) from e
