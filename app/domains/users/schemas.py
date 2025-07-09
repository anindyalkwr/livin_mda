import uuid
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from decimal import Decimal

class Account(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    balance: Decimal
    living_points: int
    holded_balance: Decimal

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    account: Optional[Account] = None

class UserInDB(User):
    hashed_password: str

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
