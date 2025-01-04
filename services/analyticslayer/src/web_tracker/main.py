from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend import routers

app = FastAPI()

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
        title="From First Principles Analytics Layer",
        description="API for website tracking and analytics.",
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
    app.include_router(routers.router, prefix="")

    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=5000)