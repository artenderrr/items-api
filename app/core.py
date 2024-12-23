import os
import json
from typing import cast
from fastapi.encoders import jsonable_encoder
from app.schemas import Item, UpdatedItemFields

class ItemManager:
    def __init__(self, path_to_items: str = "app/data"):
        self.path_to_items = path_to_items

    @property
    def item_ids(self) -> list[int]:
        """ Get all existing item IDs """
        item_files = os.listdir(self.path_to_items)
        return [int(i.split(".")[0]) for i in item_files]
    
    def get_item_file_path(self, item_id: int) -> str:
        """ Generate item file path based on given ID """
        return f"{self.path_to_items}/{item_id}.json"
    
    def item_id_exists(self, item_id: int) -> bool:
        """ Check if an item with the specified ID exists """
        item_file_path = self.get_item_file_path(item_id)
        return os.path.isfile(item_file_path)

    def get_item(self, item_id: int) -> Item | None:
        """ Retrieve item by its ID """
        try:
            item_file_path = self.get_item_file_path(item_id)
            with open(item_file_path, encoding="utf-8") as file:
                return Item(**json.load(file))
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
    
    def create_item(self, item_id: int, item: Item) -> bool:
        """ Create new item from given model and return completion status """
        if self.item_id_exists(item_id):
            return False
        new_item_file_path = self.get_item_file_path(item_id)
        with open(new_item_file_path, "w") as file:
            json_compatible_item_data = jsonable_encoder(item)
            json.dump(json_compatible_item_data, file, indent=4)
        return True
    
    def update_item(self, item_id: int, updated_item_fields: UpdatedItemFields) -> bool:
        """ Update existing item with updated values provided and return completion status """
        if not self.item_id_exists(item_id):
            return False
        old_item = cast(Item, self.get_item(item_id))
        updated_item_dict = old_item.model_dump() | updated_item_fields.model_dump(exclude_defaults=True)
        self.delete_item(item_id)
        self.create_item(item_id, Item(**updated_item_dict))
        return True
    
    def delete_item(self, item_id: int) -> bool:
        """ Delete existing item and return completion status """
        if not self.item_id_exists(item_id):
            return False
        item_file_path = self.get_item_file_path(item_id)
        os.remove(item_file_path)
        return True