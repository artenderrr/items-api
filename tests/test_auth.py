from fastapi.testclient import TestClient
from app.main import app
from tests.helpers import auth_headers

client = TestClient(app)

class TestAuth:
    def test_without_key(self) -> None:
        response = client.get("/items")
        assert response.status_code == 403

    def test_with_invalid_key(self) -> None:
        response = client.get("/items", headers={"X-Key": "some_invalid_key"})
        assert response.status_code == 401

    def test_with_valid_key(self) -> None:
        response = client.get("/items", headers=auth_headers)
        assert response.status_code == 200