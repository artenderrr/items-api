import os
import json
from app.schemas import Item

class ItemManager:
    def __init__(self, path_to_items: str = "app/data"):
        self.path_to_items = path_to_items

    @property
    def item_ids(self) -> list[int]:
        item_file_names = os.listdir(self.path_to_items)
        return [int(i.split(".")[0]) for i in item_file_names]

    def get_item(self, item_id: int) -> Item | None:
        """ Retrieve item by its ID """
        try:
            path_to_item = f"{self.path_to_items}/{item_id}.json"
            with open(path_to_item, encoding="utf-8") as f:
                return Item(**json.load(f))
        except FileNotFoundError:
            return None
        
    def get_items(self, category: str | None = None) -> list[Item]:
        """ Retrieve all items or items that are in the specified category """
        items: list[Item] = []
        for item_id in self.item_ids:
            item = self.get_item(item_id)
            if item and (category is None or item.category == category):
                items.append(item)
        return items