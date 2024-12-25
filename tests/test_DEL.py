import random
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.helpers import auth_headers, item_manager, test_items
from tests.helpers import restore_default_items

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_cleanup_items():
    item_manager.delete_all_items()
    yield
    restore_default_items()

@pytest.fixture
def random_item_id():
    return random.randint(1, 100)

@pytest.fixture
def random_item():
    return random.choice([*test_items.values()])

class TestDEL:
    def test_deleting_existing_item(self, random_item_id, random_item):
        item_manager.create_item(random_item_id, random_item)
        response = client.delete(f"/items/{random_item_id}", headers=auth_headers)
        assert response.status_code == 204
        assert item_manager.get_item(random_item_id) is None

    def test_deleting_not_existing_item(self, random_item_id):
        response = client.delete(f"/items/{random_item_id}", headers=auth_headers)
        assert response.status_code == 404