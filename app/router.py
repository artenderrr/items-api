from typing import Annotated
from fastapi import APIRouter
from fastapi import Path, HTTPException
from app.schemas import Item
from app.core import ItemManager

router = APIRouter()

@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}

@router.get("/items/{item_id}")
def get_item(item_id: Annotated[int, Path(gt=0)]) -> Item:
    item = ItemManager().get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item