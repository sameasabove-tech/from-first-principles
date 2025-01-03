"""
This module defines a Flask Blueprint for serving the index page of the application.

It provides a simple route that renders the 'index.html' template.
"""

from flask import Blueprint
from flask import Response
from flask import render_template


# Define Blueprint
index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def handle_index() -> Response:
    """
    Route for the index page. Renders the 'index.html' template.

    Returns:
        Response: The rendered HTML content of the index page.
    """
    return render_template("index.html")
