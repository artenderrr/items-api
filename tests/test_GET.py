import pytest
from fastapi.testclient import TestClient
from app.core import ItemManager
from app.main import app
from tests.helpers import auth_headers, test_items, default_items

client = TestClient(app)
item_manager = ItemManager()

def populate_items(item_list):
    for item_id, item in enumerate(item_list, start=1):
        item_manager.create_item(item_id, item)

def restore_default_items():
    item_manager.delete_all_items()
    populate_items(default_items)

@pytest.fixture(autouse=True)
def setup_and_cleanup_items():
    item_manager.delete_all_items()
    yield
    restore_default_items()

class TestGET:
    @pytest.mark.parametrize(
            ["test_items_list"],
            [
                ([],),
                ([test_items["Apple"]],),
                ([*test_items.values()],)
            ]
    )
    def test_getting_all_items(self, test_items_list):
        populate_items(test_items_list)
        response = client.get("/items", headers=auth_headers)
        received_items = sorted(response.json(), key=lambda x: x["name"])
        expected_items = sorted((item.model_dump() for item in test_items_list), key=lambda x: x["name"])
        assert response.status_code == 200
        assert received_items == expected_items

    @pytest.mark.parametrize(
            ["test_items_list", "category"],
            [
                ([test_items["Apple"], test_items["Banana"], test_items["Notebook"]], "food"),
                ([*test_items.values()], "electronics"),
                ([*test_items.values()], "non_existent_category")
            ]
    )
    def test_getting_all_items_by_category(self, test_items_list, category):
        populate_items(test_items_list)
        response = client.get(f"/items?category={category}", headers=auth_headers)
        received_items = sorted(response.json(), key=lambda x: x["name"])
        expected_items = sorted(
            (item.model_dump() for item in test_items_list if item.category == category),
            key=lambda x: x["name"]
        )
        assert response.status_code == 200
        assert received_items == expected_items

    @pytest.mark.parametrize(
            ["item_id", "item", "expected_status_code", "expected_response_body"],
            [
                (1, test_items["Apple"], 200, test_items["Apple"].model_dump()),
                ("foo", test_items["Backpack"], 422, None),
                (0, test_items["Banana"], 422, None),
                (1, None, 404, None)
            ]
    )
    def test_getting_one_item(self, item_id, item, expected_status_code, expected_response_body):
        if item and type(item_id) is int and item_id > 0:
            item_manager.create_item(item_id, item)
        response = client.get(f"/items/{item_id}", headers=auth_headers)
        assert response.status_code == expected_status_code
        if expected_status_code == 200:
            assert response.json() == expected_response_body