from typing import Annotated, cast
from fastapi import APIRouter
from fastapi import Path, Query, Body, HTTPException
from app.schemas import Item, UpdatedItemFields
from app.core import ItemManager
from app.examples import RequestExamples
from app.examples import ResponseExamples

router = APIRouter(tags=["items"])

ValidItemID = Annotated[int, Path(
    description="Unique ID of an item.",
    gt=0,
    openapi_examples=RequestExamples.item_id
)]

@router.get("/items", summary="Retrieve all existing items")
def get_items(
    category: Annotated[str | None, Query(
        description="Category of items to retrieve.",
        openapi_examples=RequestExamples.category
    )] = None
) -> list[Item]:
    items = ItemManager().get_items(category)
    return items

@router.get(
    "/items/{item_id}",
    summary="Retrieve specific item by its ID",
    responses={404: ResponseExamples.item_not_found}
)
def get_item(item_id: ValidItemID) -> Item:
    item = ItemManager().get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item with specified ID doesn't exist")
    return item

@router.post(
    "/items/{item_id}",
    status_code=201,
    summary="Create new item",
    responses={409: ResponseExamples.item_already_exists}
)
def create_item(
    item_id: ValidItemID,
    item: Annotated[Item, Body(
        openapi_examples=RequestExamples.item
    )]
) -> Item:
    success = ItemManager().create_item(item_id, item)
    if not success:
        raise HTTPException(status_code=409, detail="Item with specified ID already exists")
    return item

@router.put(
    "/items/{item_id}",
    summary="Modify existing item",
    responses={404: ResponseExamples.item_not_found}
)
def update_item(
    item_id: ValidItemID,
    updated_item_fields: Annotated[UpdatedItemFields, Body(
        openapi_examples=RequestExamples.updated_item_fields
    )]
) -> Item:
    success = ItemManager().update_item(item_id, updated_item_fields)
    if not success:
        raise HTTPException(status_code=404, detail="Item with specified ID doesn't exist")
    return cast(Item, ItemManager().get_item(item_id))

@router.delete(
    "/items/{item_id}",
    status_code=204,
    summary="Remove existing item",
    responses={404: ResponseExamples.item_not_found}
)
def delete_item(item_id: ValidItemID) -> None:
    success = ItemManager().delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item with specified ID doesn't exist")
    return None