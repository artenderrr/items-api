from typing import Annotated
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: str
    category: str
    quantity: Annotated[int, Field(gt=0)]