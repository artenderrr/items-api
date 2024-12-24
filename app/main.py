from fastapi import FastAPI
from fastapi import Depends
from app.security import verify_api_key
from app.router import router

tags_metadata = [
    {
        "name": "items",
        "description": "Manage items."
    }
]

app = FastAPI(
    title="Items API",
    summary="Simple CRUD API to manage items.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    dependencies=[Depends(verify_api_key)]
)

app.include_router(router)