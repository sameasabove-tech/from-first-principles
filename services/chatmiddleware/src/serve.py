"""
Entry point for the application.

This script creates a Flask application using a custom middleware creation function
and starts the development server.
"""
from flask import Flask  # Optional import for type hinting

from appfactory import create_middleware_app


# Create the Flask application with middleware
app: Flask = create_middleware_app()


def run_server():
    app.run(debug=True, port=8080)


if __name__ == "__main__":
    run_server()  # Run the development server
