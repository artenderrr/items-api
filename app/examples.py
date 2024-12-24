class RequestExamples:
    item_id = {
        "normal": {
            "summary": "Valid ID",
            "value": 1
        },
        "invalid": {
            "summary": "Invalid ID",
            "value": "foo"
        }
    }
    category = {
            "normal": {
                "summary": "Valid category",
                "value": "tech"
            },
            "invalid": {
                "summary": "Invalid category",
                "value": 123
            }
        }
    item = {
            "normal": {
                "summary": "Valid item",
                "description": "A valid item should contain all of the necessary fields with correct value types.",
                "value": {
                    "name": "Banana",
                    "description": "Yellow tropical fruit",
                    "category": "food",
                    "quantity": 3
                }
            },
            "invalid": {
                "summary": "Invalid item",
                "description": "Invalid items are rejected at creation.",
                "value": {
                    "name": 123,
                    "foobar": [1, 2, 3],
                    "category": True,
                    "quantity": -5
                }
            }
        }
    updated_item_fields = {
            "normal": {
                "summary": "Valid update fields",
                "description": ("To modify an item, at least one valid field must be provided. " + 
                                "As a result, the provided fields will be modified, while the other fields of the item will remain unchanged."
                                ),
                "value": {
                    "name": "Daiquiri",
                    "category": "drinks"
                }
            },
            "invalid": {
                "summary": "Invalid update fields",
                "description": "Update fields are considered invalid if they are empty or contain invalid key-value pairs.",
                "value": {}
            }
        }

class ResponseExamples:
    item_not_found = {
                "description": "Item Not Found",
                "content": {
                    "application/json": {
                        "example": {"detail": "Item with specified ID doesn't exist"}
                    }
                }
            }
    item_already_exists = {
                "description": "Item Already Exists",
                "content": {
                    "application/json": {
                        "example": {"detail": "Item with specified ID already exists"}
                    }
                }
            }