import uuid
from pydantic import BaseModel, ConfigDict
from typing import List

class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    label: str

class CategoryList(BaseModel):
    items: List[Category]
    total: int
    page: int
    size: int