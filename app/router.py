from typing import Annotated
from fastapi import APIRouter
from fastapi import Path, HTTPException
from app.schemas import Item
from app.core import ItemManager

router = APIRouter()

@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}

@router.get("/items")
def get_items(category: str | None = None) -> list[Item]:
    items = ItemManager().get_items(category)
    return items

@router.get("/items/{item_id}")
def get_item(item_id: Annotated[int, Path(gt=0)]) -> Item:
    item = ItemManager().get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items/{item_id}", status_code=201)
def create_item(item_id: Annotated[int, Path(gt=0)], item: Item) -> Item:
    success = ItemManager().create_item(item_id, item)
    if not success:
        raise HTTPException(status_code=409, detail="Item with specified ID already exists")
    return item

@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: Annotated[int, Path(gt=0)]) -> None:
    success = ItemManager().delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item with specified ID doesn't exist")
    return None