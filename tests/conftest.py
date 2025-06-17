import sys
import os
import pytest


# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Object_detection_api import app as flask_app


@pytest.fixture
def Object_detection_api():
    """Fixture to provide the Flask app for testing."""
    flask_app.config.update({"TESTING": True})
    yield flask_app


@pytest.fixture
def client(app):
    """Fixture to provide a test client for the Flask app."""
    return app.test_client()
