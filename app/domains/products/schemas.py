import uuid
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

class CategoryInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    label: str

class MerchantInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str

class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    amount: Decimal
    stock: int
    category: Optional[CategoryInfo] = None
    merchant: Optional[MerchantInfo] = None
    created_at: datetime

class ProductList(BaseModel):
    items: List[Product]
    total: int
    page: int
    size: int