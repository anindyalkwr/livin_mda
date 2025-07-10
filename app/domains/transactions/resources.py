from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, cast, Date
from typing import Tuple, Optional, List
import uuid
from datetime import date, timedelta
import math

from . import schemas
from app.database.models import Account, Product, Transaction, User, Category

def create_deposit(db: Session, user_id: uuid.UUID, deposit: schemas.DepositCreate) -> Transaction:
    """
    Handles depositing money into a user's account within a single transaction.
    """
    try:
        account = db.query(Account).filter(Account.user_id == user_id).with_for_update().one()
        account.balance += deposit.amount
        db_transaction = Transaction(
            user_id=user_id,
            total_amount=deposit.amount,
            status='completed',
            transaction_type='deposit'
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise e


def create_payment(db: Session, user_id: uuid.UUID, payment: schemas.PaymentCreate) -> Tuple[Optional[Transaction], Optional[str]]:
    """
    Handles a product payment within a single, atomic database transaction.
    This now includes logic to add living points.
    """
    try:
        account = db.query(Account).filter(Account.user_id == user_id).with_for_update().one()
        product = db.query(Product).filter(Product.id == payment.product_id).with_for_update().first()

        if not product:
            db.rollback()
            return None, "Product not found."

        if product.stock < payment.quantity:
            db.rollback()
            return None, f"Insufficient stock for {product.name}. Available: {product.stock}, Requested: {payment.quantity}."

        total_cost = product.amount * payment.quantity
        if account.balance < total_cost:
            db.rollback()
            return None, f"Insufficient balance. Required: {total_cost}, Available: {account.balance}."

        account.balance -= total_cost

        product.stock -= payment.quantity
        
        points_to_add = math.floor(total_cost * Decimal('0.01'))
        account.living_points += points_to_add

        db_transaction = Transaction(
            user_id=user_id,
            product_id=payment.product_id,
            quantity=payment.quantity,
            total_amount=total_cost,
            status='completed',
            transaction_type='payment'
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction, None
    except Exception as e:
        db.rollback()
        return None, "An unexpected error occurred during the transaction."


def get_transaction_by_id(db: Session, transaction_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Transaction]:
    """
    Fetches a single transaction by its ID, ensuring it belongs to the requesting user.
    Eagerly loads product and category info.
    """
    return (
        db.query(Transaction)
        .options(joinedload(Transaction.product).joinedload(Product.category))
        .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
        .first()
    )


def get_user_transactions(
    db: Session,
    user_id: uuid.UUID,
    page: int,
    size: int,
    category_label: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Tuple[List[Transaction], int]:
    """
    Fetches a paginated and filtered list of transactions for a specific user.
    """
    offset = (page - 1) * size
    
    query = (
        db.query(Transaction)
        .options(joinedload(Transaction.product).joinedload(Product.category))
        .filter(Transaction.user_id == user_id)
    )

    if category_label:
        query = query.join(Product).join(Category).filter(Category.label == category_label)
    
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
        
    if end_date:
        from datetime import timedelta
        query = query.filter(Transaction.transaction_date < (end_date + timedelta(days=1)))

    total = query.count()
    items = query.order_by(desc(Transaction.transaction_date)).offset(offset).limit(size).all()
    
    return items, total

def get_amount_per_category(db: Session, user_id: uuid.UUID, start_date: Optional[date], end_date: Optional[date]) -> List[Tuple[str, Decimal]]:
    query = (
        db.query(
            Category.label,
            func.sum(Transaction.total_amount).label("total_amount")
        )
        .join(Product, Transaction.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        .filter(Transaction.user_id == user_id)
        .filter(Transaction.transaction_type == 'payment')
        .group_by(Category.label)
        .order_by(desc("total_amount"))
    )
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date < (end_date + timedelta(days=1)))
    
    return query.all()

def get_count_per_category(db: Session, user_id: uuid.UUID, start_date: Optional[date], end_date: Optional[date]) -> List[Tuple[str, int]]:
    query = (
        db.query(
            Category.label,
            func.count(Transaction.id).label("transaction_count")
        )
        .join(Product, Transaction.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        .filter(Transaction.user_id == user_id)
        .filter(Transaction.transaction_type == 'payment')
        .group_by(Category.label)
        .order_by(desc("transaction_count"))
    )
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date < (end_date + timedelta(days=1)))
        
    return query.all()

def get_time_series_data(db: Session, user_id: uuid.UUID, start_date: date, end_date: date) -> List[Tuple[date, int, Decimal]]:
    query = (
        db.query(
            cast(Transaction.transaction_date, Date).label("date"),
            func.count(Transaction.id).label("transaction_count"),
            func.sum(Transaction.total_amount).label("total_amount")
        )
        .filter(Transaction.user_id == user_id)
        .filter(cast(Transaction.transaction_date, Date).between(start_date, end_date))
        .group_by("date")
        .order_by("date")
    )
    return query.all()
