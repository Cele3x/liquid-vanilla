from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.config import settings

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_cors_middleware():
    response = client.options(
        "/recipes",
        headers={
            "Origin": settings.ALLOWED_REQUEST_URLS[0],
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert response.headers["Access-Control-Allow-Origin"] == settings.ALLOWED_REQUEST_URLS[0]
