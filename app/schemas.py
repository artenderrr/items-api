from typing import Annotated, Self
from pydantic import BaseModel, Field
from pydantic import model_validator

class Item(BaseModel):
    name: str
    description: str
    category: str
    quantity: Annotated[int, Field(gt=0)]

class UpdatedItemFields(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    quantity: Annotated[int | None, Field(gt=0)] = None

    @model_validator(mode="after")
    def require_at_least_one_field_present(self) -> Self:
        if not any(self.model_dump().values()):
            raise ValueError("At least one field must be provided")
        return self