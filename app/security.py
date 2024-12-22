from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "super_secret"
header_scheme = APIKeyHeader(name="x-key")

def verify_api_key(key: Annotated[str, Depends(header_scheme)]) -> None:
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API-key")