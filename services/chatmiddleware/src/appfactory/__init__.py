"""
Application factory for creating a Flask application with CORS and environment variables.

This module defines a function `create_middleware_app` that sets up a Flask application
with CORS enabled for all origins, loads environment variables from a '.env' file, and
registers blueprints from the 'routes' package.

Raises:
    RuntimeError: If '.env' file is missing or there's an error loading environment variables.
"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os


def create_middleware_app() -> Flask:
    """
    Creates a Flask application with CORS and environment variables.

    Loads environment variables from a '.env' file, enables CORS for all origins,
    and registers blueprints from the 'routes' package.

    Returns:
        Flask: The configured Flask application.
    """

    try:
        load_dotenv()
    except FileNotFoundError:
        raise RuntimeError("'.env' file not found. Please create one for environment variables.") from None

    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS from all origins

    # Register Blueprints (assuming routes.chat and routes.landing exist)
    from routes.chat import chat_bp
    from routes.landing import index_bp

    app.register_blueprint(chat_bp)
    app.register_blueprint(index_bp)

    return app