# tests/test_conftest.py
from fastapi.testclient import TestClient
from app.main import app  # FastAPI app import
from database import get_db_connection

# Create the test client
client = TestClient(app)

def test_client_fixture(client):
    """
    Test that the 'client' fixture (a FastAPI TestClient) works as expected.
    Here, we call the auto-generated documentation endpoint provided by FastAPI (/docs)
    and check for a successful response.
    """
    response = client.get("/docs")
    assert response.status_code == 200, "Expected /docs to be accessible (status 200)"

def test_db_session_fixture(get_db_connection):
    """
    Test that the 'get_db_connection' fixture provides a valid SQLAlchemy session.
    We simply assert that the session object is not None.
    More elaborate tests could involve performing a simple query,
    but this basic check confirms that the fixture is providing a session.
    """
    assert get_db_connection is not None, "Expected a valid SQLAlchemy session from the fixture"
