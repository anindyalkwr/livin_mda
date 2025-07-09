import uuid
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class CategoryInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    label: str

class Offer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    category: Optional[CategoryInfo] = None

class OfferList(BaseModel):
    items: List[Offer]
    total: int
    page: int
    size: int