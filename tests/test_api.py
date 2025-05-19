from fastapi.testclient import TestClient
from src.backend.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Welcome to the CID Detection API.",
    }
