from fastapi import FastAPI
from fastapi import Depends
from app.security import verify_api_key
from app.router import router

app = FastAPI(
    dependencies=[Depends(verify_api_key)]
)

app.include_router(router)