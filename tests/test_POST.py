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

class TestPOST:
    def test_creating_item_with_new_id(self, random_item_id, random_item):
        response = client.post(f"/items/{random_item_id}", json=random_item.model_dump(), headers=auth_headers)
        assert response.status_code == 201
        assert item_manager.get_item(random_item_id) == random_item

    def test_creating_item_with_existing_id(self, random_item_id, random_item):
        item_manager.create_item(random_item_id, random_item)
        response = client.post(f"/items/{random_item_id}", json=random_item.model_dump(), headers=auth_headers)
        assert response.status_code == 409