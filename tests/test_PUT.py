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

@pytest.fixture
def random_update_fields(random_item):
    update_fields = {}
    for i in range(random.randint(1, 4)):
        while (field_name := random.choice(["name", "description", "category", "quantity"])) in update_fields:
            continue
        update_fields[field_name] = random_item.model_dump()[field_name]
    return update_fields

class TestPUT:
    def test_updating_existing_item(self, random_item_id, random_item, random_update_fields):
        item_manager.create_item(random_item_id, random_item)
        response = client.put(f"/items/{random_item_id}", json=random_update_fields, headers=auth_headers)
        assert response.status_code == 200
        updated_item = item_manager.get_item(random_item_id).model_dump()
        expected_item = random_item.model_dump() | random_update_fields
        assert updated_item == expected_item
    
    def test_updating_non_existing_item(self):
        response = client.put("/items/1", json={"name": "nonexistent"}, headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.parametrize(
            ["invalid_update_fields"],
            [
                ({},),
                ({"invalid-key": "invalid-value"},),
                ({"name": None, "description": None},)
            ]
    )
    def test_updating_with_invalid_update_fields(self, random_item_id, random_item, invalid_update_fields):
        item_manager.create_item(random_item_id, random_item)
        response = client.put(f"/items/{random_item_id}", json=invalid_update_fields, headers=auth_headers)
        assert response.status_code == 422
        response_error_message = response.json()["detail"][0]["msg"]
        assert response_error_message == "Value error, At least one field must be provided"