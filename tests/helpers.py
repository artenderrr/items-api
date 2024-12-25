from app.schemas import Item
from app.security import API_KEY
from app.core import ItemManager

auth_headers = {"X-Key": API_KEY}
item_manager = ItemManager()

default_items = [
    Item(
        name="Banana",
        description="Yellow tropical fruit",
        category="food",
        quantity=3
    ),
    Item(
        name="MacBook Air M2",
        description="Powerful machine for software development",
        category="tech",
        quantity=1
    ),
    Item(
        name="Book",
        description="Gate to another world",
        category="entertainment",
        quantity=1
    )
]

test_items = {
    "Apple": Item(
        name="Apple",
        description="Red juicy fruit",
        category="food",
        quantity=2
    ),
    "Banana": Item(
        name="Banana",
        description="Yellow tropical fruit",
        category="food",
        quantity=6
    ),
    "Notebook": Item(
        name="Notebook",
        description="A ruled paper notebook",
        category="stationery",
        quantity=3
    ),
    "Pencil": Item(
        name="Pencil",
        description="A graphite writing tool",
        category="stationery",
        quantity=10
    ),
    "Chair": Item(
        name="Chair",
        description="Wooden chair for seating",
        category="furniture",
        quantity=4
    ),
    "Bottle": Item(
        name="Bottle",
        description="Reusable water bottle",
        category="accessory",
        quantity=1
    ),
    "T-shirt": Item(
        name="T-shirt",
        description="Cotton casual wear",
        category="clothing",
        quantity=5
    ),
    "Headphones": Item(
        name="Headphones",
        description="Over-ear noise-canceling headphones",
        category="electronics",
        quantity=2
    ),
    "Lamp": Item(
        name="Lamp",
        description="LED desk lamp",
        category="electronics",
        quantity=1
    ),
    "Backpack": Item(
        name="Backpack",
        description="Durable hiking backpack",
        category="accessory",
        quantity=2
    )
}

def populate_items(item_list):
    for item_id, item in enumerate(item_list, start=1):
        item_manager.create_item(item_id, item)

def restore_default_items():
    item_manager.delete_all_items()
    populate_items(default_items)