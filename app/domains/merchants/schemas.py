import uuid
from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class Merchant(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    created_at: datetime

class MerchantList(BaseModel):
    items: List[Merchant]
    total: int
    page: int
    size: int