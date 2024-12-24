from typing import Annotated, cast
from fastapi import APIRouter
from fastapi import Path, HTTPException
from app.schemas import Item, UpdatedItemFields
from app.core import ItemManager

router = APIRouter(tags=["items"])

@router.get("/items", summary="Retrieve all existing items")
def get_items(category: str | None = None) -> list[Item]:
    items = ItemManager().get_items(category)
    return items

@router.get("/items/{item_id}", summary="Retrieve specific item by its ID")
def get_item(item_id: Annotated[int, Path(gt=0)]) -> Item:
    item = ItemManager().get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items/{item_id}", status_code=201, summary="Create new item")
def create_item(item_id: Annotated[int, Path(gt=0)], item: Item) -> Item:
    success = ItemManager().create_item(item_id, item)
    if not success:
        raise HTTPException(status_code=409, detail="Item with specified ID already exists")
    return item

@router.put("/items/{item_id}", summary="Modify existing item")
def update_item(item_id: Annotated[int, Path(gt=0)], updated_item_fields: UpdatedItemFields) -> Item:
    success = ItemManager().update_item(item_id, updated_item_fields)
    if not success:
        raise HTTPException(status_code=404, detail="Item with specified ID doesn't exist")
    return cast(Item, ItemManager().get_item(item_id))

@router.delete("/items/{item_id}", status_code=204, summary="Remove existing item")
def delete_item(item_id: Annotated[int, Path(gt=0)]) -> None:
    success = ItemManager().delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item with specified ID doesn't exist")
    return None