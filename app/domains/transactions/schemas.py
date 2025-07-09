import uuid
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, date

class DepositCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, description="The amount to deposit, must be positive.")

class PaymentCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(..., gt=0, description="The quantity to purchase, must be positive.")


class CategoryInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    label: str

class ProductInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    category: Optional[CategoryInfo] = None



class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    quantity: Optional[int] = None
    total_amount: Decimal
    status: str
    transaction_date: datetime
    transaction_type: str = Field(..., description="Type of transaction, e.g., 'deposit' or 'payment'")
    
    product: Optional[ProductInfo] = None

class TransactionHistory(BaseModel):
    items: List[Transaction]
    total: int
    page: int
    size: int

class AmountPerCategory(BaseModel):
    category: str
    total_amount: Decimal

class CountPerCategory(BaseModel):
    category: str
    transaction_count: int

class TimeSeriesDataPoint(BaseModel):
    date: date
    transaction_count: int
    total_amount: Decimal

class TimeSeriesResponse(BaseModel):
    data: List[TimeSeriesDataPoint]
