import json
from app.schemas import Item

class ItemManager:
    def __init__(self, path_to_items: str = "app/data"):
        self.path_to_items = path_to_items

    def get_item(self, item_id: int) -> Item | None:
        """ Retrieve item by its ID """
        try:
            path_to_item = f"{self.path_to_items}/{item_id}.json"
            with open(path_to_item, encoding="utf-8") as f:
                return Item(**json.load(f))
        except FileNotFoundError:
            return None