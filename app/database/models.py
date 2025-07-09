import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    ForeignKey,
    TIMESTAMP,
    func
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(100), nullable=False)
    address = Column(Text)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="user", uselist=False, cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    balance = Column(Numeric(15, 2), nullable=False, default=0.00)
    living_points = Column(Integer, nullable=False, default=0)
    holded_balance = Column(Numeric(15, 2), nullable=False, default=0.00)

    user = relationship("User", back_populates="account")

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="merchant")

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String(50), unique=True, nullable=False)

    products = relationship("Product", back_populates="category")
    offers = relationship("Offer", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    merchant_id = Column(UUID(as_uuid=True), ForeignKey("merchants.id"))
    amount = Column(Numeric(15, 2), nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="products")
    merchant = relationship("Merchant", back_populates="products")
    transactions = relationship("Transaction", back_populates="product")

class Offer(Base):
    __tablename__ = "offers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))

    category = relationship("Category", back_populates="offers")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True)
    quantity = Column(Integer, nullable=True)
    total_amount = Column(Numeric(15, 2), nullable=False)
    status = Column(String(20), default='completed')
    transaction_type = Column(String(20), nullable=False)
    transaction_date = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="transactions")
    product = relationship("Product", back_populates="transactions")
