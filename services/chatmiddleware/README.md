


# Chat Middleware (Backend Service for AI Chatbot)

 ![versions](https://img.shields.io/badge/python-3.13-blue?logo=python)
[![codecov](https://codecov.io/gh/justmeloic/from-first-principles/graph/badge.svg?token=4GYOJ42J2C)](https://codecov.io/gh/justmeloic/from-first-principles)
![Static Badge](https://img.shields.io/badge/build-passing-brightgreen)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](https://opensource.org/licenses/Apache-2.0)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/justmeloic/From-First-Principles/issues)
[![GitHub issues](https://img.shields.io/github/issues/justmeloic/From-First-Principles)](https://github.com/justmeloic/From-First-Principles/issues)
[![GitHub stars](https://img.shields.io/github/stars/justmeloic/From-First-Principles)](https://github.com/justmeloic/From-First-Principles/stargazers)


This service is the **middleware backend** for an AI chatbot integrated into a website. It's built with **FastAPI** and serves as the intermediary between the website's frontend and a contextually fine-tuned generative AI model (currently Gemini Pro). The AI model is specifically tuned using the website's content, enabling it to provide relevant and accurate responses related to the site. It also uses **Redis** to store and retrieve conversation history, allowing for context-aware interactions.

**[Loïc Muhirwa](https://github.com/justmeloic/)** initiated this project, and we enthusiastically welcome contributions from the community.

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
*   **Processes and validates requests:** The service processes incoming requests, ensuring they are in the correct format and contain the necessary information. It uses Pydantic models for data validation.
*   **Interacts with the fine-tuned Gemini Pro model:** It communicates with the Gemini Pro model, which has been specifically trained on the website's content. This allows the chatbot to provide answers and engage in conversations that are directly related to the information available on the website.
*   **Manages conversation history with Redis:** The service stores and retrieves conversation history from a Redis database. Each conversation is associated with a unique ID, allowing the chatbot to maintain context and provide more relevant responses.
*   **Formats and returns responses:** The service formats the AI model's responses into a suitable format for the website's frontend to display to the user.
*   **Provides a simple landing page:** Offers a basic landing page (`/`) for status checks or general information.

**Key Features:**

*   **Built with FastAPI:** Leverages the FastAPI framework for a high-performance and efficient backend.
*   **Contextually-Aware AI:** Uses a generative AI model (Gemini Pro) fine-tuned on the website's content for relevant responses.
*   **Conversation History:** Employs Redis to store and retrieve conversation history, enabling context-aware interactions.
*   **Asynchronous Operations:** Designed for asynchronous operations using `async` and `await` to handle requests efficiently.
*   **Configurable Routes:** Easy to extend with additional routes and features to support the evolving needs of the chatbot.
*   **Data Validation:** Uses Pydantic models to ensure the integrity and correctness of the data exchanged.

## Directory Structure

## Directory Structure


```
chatmiddleware/
├── README.md           # This file
├── pyproject.toml      # Project configuration (dependencies, build settings)
├── run-tests.sh        # Script to run tests
├── src/                # Source code
│   ├── models/
│   │   └── chat_model.py # Data models for chat interactions
│   ├── routers/
│   │   ├── chat_routers.py       # Chat endpoint logic (handles requests to the AI model)
│   │   └── landing_routers.py    # Landing page endpoint
│   ├── main.py          # Main application entry point
│   └── templates/
│       └── index.html    # Template for the landing page
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
*   **Redis Server:** You need a running Redis server for conversation history. Install and run it locally or use a cloud-hosted instance.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/justmeloic/from-first-principles.git](https://github.com/justmeloic/from-first-principles.git)
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

1.  **Set Environment Variables:**

    You need to set the following environment variables before running the application or tests:

    *   `GEMINI_API_KEY`: Your Gemini API key.
    *   `REDIS_HOST`: The hostname or IP address of your Redis server (default: `127.0.0.1`).
    *   `REDIS_PORT`: The port number of your Redis server (default: `6379`).
    *   `REDIS_DB`: The Redis database number to use (default: `0`).

    **Using a `.env` file (Recommended for development):**

    *   Create a `.env` file in the `services/chatmiddleware` directory:

        ```
        GEMINI_API_KEY=your_api_key
        REDIS_HOST=127.0.0.1
        REDIS_PORT=6379
        REDIS_DB=0
        ```

    *   Install `python-dotenv`: `uv pip install python-dotenv`
    *   Load the environment variables in your application (e.g., in `main.py`):

        ```python
        from dotenv import load_dotenv
        import os

        load_dotenv()

        # ... rest of your code
        ```

    *   **Important:** Add `.env` to your `.gitignore` file to prevent committing sensitive information.

    **Temporarily in your terminal:**

    ```bash
    export GEMINI_API_KEY="your_api_key"  # Linux/macOS
    set GEMINI_API_KEY="your_api_key"  # Windows
    # Similarly for REDIS_HOST, REDIS_PORT, and REDIS_DB
    ```

    **In your CI/CD environment (e.g., GitHub Actions):**

    *   Store the API key and Redis connection details as secrets in your repository settings.
    *   Make the secrets available as environment variables in your workflow (see example in the Testing section).

## Running the Application
### Running Redis Server

Before running the application, ensure you have a Redis server running.


## Local Installation
You can install Redis locally on your system. Follow the instructions for your operating system from the official Redis website: https://redis.io/download

Once installed, start the Redis server using:
```bash
redis-server
```

By default, Redis will listen on port 6379.

Verifying Redis is Running
You can check if Redis is running by using the redis-cli tool:

If Redis is running, it should respond with `PONG`.

1.  **Run the `main.py` script:**

    ```bash
    uv run uvicorn src.main:app --reload
    ```

    This will start the Uvicorn server, which runs your FastAPI application. The `--reload` flag enables hot reloading, so the server will automatically restart when you make changes to your code.

2.  **Access the application:**

      * Open your web browser and go to `http://127.0.0.1:8000/`. You should see the landing page.
      * To interact with the chat endpoint, send a POST request to `http://127.0.0.1:8000/api/v1/chat`.
      * You can also access the automatically generated API documentation at `http://127.0.0.1:8000/docs` (Swagger UI) or `http://127.0.0.1:8000/redoc` (ReDoc).

**Note:** The `main.py` script is intended for local development. For production deployments, you should use a production-ready ASGI server like Uvicorn or Hypercorn, along with a process manager and potentially a reverse proxy (like Nginx).

## Testing

This project uses `pytest` for testing.

1.  **Run tests with coverage:**

    ```bash
    source run-tests.sh
    ```

2.  **View the HTML coverage report:**

      * Open the `coverage-report/index.html` file in your browser.

**GitHub Actions (CI/CD):**

The GitHub Actions workflow (`chatmiddleware-ci.yml`) automatically runs tests and uploads coverage reports to Codecov on pushes to `main` or `dev` and on pull requests against `main`.

  * **Codecov:** Sign up for a free Codecov account and connect your repository.
  * **Secrets:**
      * `GEMINI_API_KEY`: Store your Gemini API key as a secret.
      * `CODECOV_TOKEN` (Optional): Store a Codecov upload token if needed.

## API Documentation

The API documentation is automatically generated by FastAPI and can be accessed at:

  * `/docs`: Swagger UI - Interactive API documentation where you can try out the endpoints.
  * `/redoc`: ReDoc - Alternative API documentation format.

Here's a summary of the endpoints:

### Landing Page

  * **Path:** `/`
  * **Method:** `GET`
  * **Description:** Returns a simple HTML landing page or status message.

### Chat

  * **Path:** `/api/v1/chat`

  * **Method:** `POST`

  * **Description:** Handles chat requests, generates responses using the Gemini model, and maintains conversation history in Redis.

  * **Request Body:**

    ```json
    {
      "message": "Your message to the AI chatbot",
      "conversation_id": "Optional unique ID for the conversation"
    }
    ```

      * `message` (str, required): The user's message.
      * `conversation_id` (str, optional):  If not provided, a new conversation ID will be generated.

  * **Response:**

    ```json
    {
      "response": "The AI chatbot's response",
      "conversation_id": "Unique ID for the conversation"
    }
    ```

      * `response` (str): The AI model's generated response.
      * `conversation_id` (str): The unique ID associated with the conversation. This ID should be included in subsequent requests to maintain the conversation context.

**Example using `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "What can you tell me about this website?", "conversation_id": "my-unique-id"}' [http://127.0.0.1:8000/api/v1/chat](http://127.0.0.1:8000/api/v1/chat)
```






## Contributing

Please refer to the main project's `CONTRIBUTING_CONTENT.md` and `CONTRIBUTING_DEV.md` for guidelines on contributing to this service.

## License

This project is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). See the `LICENSE` file for details.
