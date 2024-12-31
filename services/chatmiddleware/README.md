


# Chat Middleware (Backend Service for AI Chatbot)

 ![versions](https://img.shields.io/badge/python-3.13-blue?logo=python)
[![codecov](https://codecov.io/gh/your-username/your-repo/branch/main/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/your-username/your-repo)
![Static Badge](https://img.shields.io/badge/cov-93%25-h)
![Static Badge](https://img.shields.io/badge/build-passing-brightgreen)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](https://opensource.org/licenses/Apache-2.0)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/justmeloic/From-First-Principles/issues)
[![GitHub issues](https://img.shields.io/github/issues/justmeloic/From-First-Principles)](https://github.com/justmeloic/From-First-Principles/issues)
[![GitHub stars](https://img.shields.io/github/stars/justmeloic/From-First-Principles)](https://github.com/justmeloic/From-First-Principles/stargazers)


This service is the **middleware backend** for an AI chatbot integrated into a website. It's built with **Flask** and serves as the intermediary between the website's frontend and a contextually fine-tuned generative AI model (currently Gemini Pro). The AI model is specifically tuned using the website's content, enabling it to provide relevant and accurate responses related to the site.

**[Loïc Muhirwa](https://github.com/justmeloic/)**  initiated this project, and we enthusiastically welcome contributions from the community.

## Table of Contents

*   [Overview](#overview)
*   [Directory Structure](#directory-structure)
*   [Prerequisites](#prerequisites)
*   [Installation](#installation)
*   [Configuration](#configuration)
*   [Running the Application](#running-the-application)
*   [Testing](#testing)
*   [API Documentation](#api-documentation)
*   [Contributing](#contributing)
*   [License](#license)

## Overview

The Chat Middleware service plays a crucial role in the website's AI chatbot architecture. It's designed to be a scalable and maintainable component that handles the following:

*   **Receives requests from the website's frontend:** When a user interacts with the chatbot on the website, their requests are sent to this middleware service.
*   **Processes and validates requests:** The service processes incoming requests, ensuring they are in the correct format and contain the necessary information.
*   **Interacts with the fine-tuned Gemini Pro model:** It communicates with the Gemini Pro model, which has been specifically trained on the website's content. This allows the chatbot to provide answers and engage in conversations that are directly related to the information available on the website.
*   **Formats and returns responses:** The service formats the AI model's responses into a suitable format for the website's frontend to display to the user.
*   **Provides a simple landing page:** Offers a basic landing page (`/`) for status checks or general information.

**Key Features:**

*   **Built with Flask:** Leverages the Flask framework for a lightweight and efficient backend.
*   **Contextually-Aware AI:** Uses a generative AI model (Gemini Pro) fine-tuned on the website's content for relevant responses.
*   **Asynchronous Operations:** Designed for asynchronous operations using `async` and `await` to handle requests efficiently.
*   **Configurable Routes:** Easy to extend with additional routes and features to support the evolving needs of the chatbot.

## Directory Structure


```
chatmiddleware/
├── README.md           # This file
├── coverage-report/    # HTML coverage report (generated, not tracked)
├── coverage.xml        # XML coverage report (generated, not tracked)
├── pyproject.toml      # Project configuration (dependencies, build settings)
├── run-tests.sh        # Script to run tests
├── src/                # Source code
│   ├── appfactory/
│   │   └── init.py   # Factory function to create the Flask app
│   ├── models/
│   │   └── chat_model.py # Data models for chat interactions
│   ├── routes/
│   │   ├── chat.py       # Chat endpoint logic (handles requests to the AI model)
│   │   └── landing.py    # Landing page endpoint
│   ├── serve.py          # Main application entry point (starts the Flask development server)
│   └── templates/
│       └── index.html    # Template for the landing page
├── tests/              # Unit and integration tests
│   ├── appfactory_test.py
│   ├── conftest.py       # Pytest configuration and fixtures
│   ├── models_test/
│   │   └── chat_model_test.py
│   ├── routes_test/
│   │   ├── chat_test.py
│   │   └── landing_test.py
│   └── serve_test.py
└── uv.lock             # Lock file for uv (dependencies' versions)
```

## Prerequisites

*   **Python 3.11+:** Ensure you have Python 3.11 or a later version installed.
*   **uv:** This project uses `uv` for dependency management. Install it globally using pip:

    ```bash
    python -m pip install --upgrade pip
    pip install uv
    ```
*   **Gemini API Key:** You'll need a Gemini API key to interact with the Gemini Pro model. Obtain one from Google Cloud AI Platform if you haven't already.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/justmeloic/from-first-principles.git
    cd from-first-principles/services/chatmiddleware
    ```

2.  **Create and activate a virtual environment (Recommended):**

    ```bash
    uv venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies using `uv`:**

    ```bash
    uv sync
    ```

## Configuration

1.  **Set the `GEMINI_API_KEY` Environment Variable:**

    You need to set the `GEMINI_API_KEY` environment variable before running the application or tests.

    *   **Temporarily in your terminal:**

        ```bash
        export GEMINI_API_KEY="your_api_key"  # Linux/macOS
        set GEMINI_API_KEY="your_api_key"  # Windows
        ```

    *   **Using a `.env` file (Recommended for development):**

        *   Create a `.env` file in the `services/chatmiddleware` directory:

            ```
            GEMINI_API_KEY=your_api_key
            ```
        *   Install `python-dotenv`: `uv add python-dotenv`
        *   Load the environment variables in your application (e.g., in `serve.py`):

            ```python
            from dotenv import load_dotenv
            import os

            load_dotenv()

            app = create_middleware_app()  # Assuming create_middleware_app is your Flask app factory

            # ... rest of your code
            ```

        *   **Important:** Add `.env` to your `.gitignore` file.

    *   **In your CI/CD environment (e.g., GitHub Actions):**

        *   Store the API key as a secret in your repository settings.
        *   Make the secret available as an environment variable in your workflow (see example in the Testing section).

## Running the Application

1.  **Run the `serve.py` script:**

    ```bash
    uv run src/serve.py
    ```

    This will start the Flask development server.

2.  **Access the application:**

    *   Open your web browser and go to `http://127.0.0.1:8000/`. You should see the landing page.
    *   To interact with the chat endpoint, send a POST request to `http://127.0.0.1:8000/chat`.

**Note:** The `serve.py` script is intended for local development. For production deployments, you should use a production-ready WSGI server like Gunicorn or uWSGI, along with a process manager and potentially a reverse proxy (like Nginx).

## Testing

This project uses `pytest` for testing.

1.  **Run tests with coverage:**

    ```bash
    source run-tests.sh
    ```

2.  **View the HTML coverage report:**

    *   Open the `coverage-report/index.html` file in your browser.

**GitHub Actions (CI/CD):**

The GitHub Actions workflow (`chatmiddleware-ci.yml`) automatically runs tests and uploads coverage reports to Codecov on pushes to `main` or `dev` and on pull requests against `main`.

*   **Codecov:** Sign up for a free Codecov account and connect your repository.
*   **Secrets:**
    *   `GEMINI_API_KEY`: Store your Gemini API key as a secret.
    *   `CODECOV_TOKEN` (Optional): Store a Codecov upload token if needed.

## API Documentation

*   **Landing Page (`/`)**: A simple HTML landing page or status message.
*   **Chat (`/chat`)**:
    *   **Method:** `POST`
    *   **Request Body:**
        ```json
        {
          "message": "Your message to the AI chatbot"
        }
        ```
    *   **Response:**
        ```json
        {
          "response": "The AI chatbot's response"
        }
        ```

    **Example using `curl`:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"message": "What can you tell me about this website?"}' [http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat)
    ```

## Contributing

Please refer to the main project's `CONTRIBUTING_CONTENT.md` and `CONTRIBUTING_DEV.md` for guidelines on contributing to this service.

## License

This project is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). See the `LICENSE` file for details.
