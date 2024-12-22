from fastapi import FastAPI
from fastapi import Depends
from app.security import verify_api_key

app = FastAPI(
    dependencies=[Depends(verify_api_key)]
)

@app.get("/")
def root():
    return {"message": "Hello World!"}