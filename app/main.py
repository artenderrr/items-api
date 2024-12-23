from fastapi import FastAPI
from fastapi import Depends
from app.security import verify_api_key
from app.router import router

app = FastAPI(
    title="Items API",
    summary="Simple CRUD API to manage items.",
    version="1.0.0",
    dependencies=[Depends(verify_api_key)]
)

app.include_router(router)