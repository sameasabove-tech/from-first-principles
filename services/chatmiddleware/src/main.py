"""
Main module for the FastAPI application. Creates and configures the FastAPI application.

This module sets up the FastAPI application, configures middleware,
includes routers, and starts the Uvicorn server.
"""

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import chat_router
from routers import landing_router


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    """
    try:
        load_dotenv()
    except FileNotFoundError:
        raise RuntimeError(
            "'.env' file not found. Please create one for environment variables."
        ) from None

    app = FastAPI(
        title="Chat API",
        description="API for interacting with a Gemini based Chat Model.",
        version="0.1.0",
    )

    # Configure CORS
    origins = ["*"]  # Allow all origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register application routers
    app.include_router(chat_router.router, prefix="/api/v1")
    app.include_router(landing_router.router, prefix="/api/v1")

    return app


if __name__ == "__main__":
    app = create_app()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
