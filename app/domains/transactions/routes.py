# app/domains/transactions/routes.py
import uuid
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date
from enum import Enum

from . import handlers, schemas
from app.middleware.auth import get_current_user
from app.database.models import User as UserModel

router = APIRouter()

class PageSize(int, Enum):
    five = 5
    ten = 10
    twenty = 20

@router.post("/transactions/deposit", response_model=schemas.Transaction, status_code=201)
def make_deposit(
    deposit_in: schemas.DepositCreate,
    handler: handlers.TransactionHandler = Depends(),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Deposit funds into the current user's account. Protected endpoint.
    """
    return handler.process_deposit(user_id=current_user.id, deposit=deposit_in)

@router.post("/transactions/pay", response_model=schemas.Transaction, status_code=201)
def make_payment(
    payment_in: schemas.PaymentCreate,
    handler: handlers.TransactionHandler = Depends(),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Pay for a product. This will validate balance and stock in a single transaction.
    Protected endpoint.
    """
    return handler.process_payment(user_id=current_user.id, payment=payment_in)

@router.get("/transactions", response_model=schemas.TransactionHistory)
def read_my_transactions(
    handler: handlers.TransactionHandler = Depends(),
    current_user: UserModel = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    pageSize: PageSize = Query(PageSize.ten, description="Number of items per page"),
    category: Optional[str] = Query(None, description="Filter by category label (e.g., 'Elektronik')"),
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)")
):
    """
    Retrieve transaction history for the current user with filtering and pagination.
    Protected endpoint.
    """
    return handler.get_my_transactions(
        user_id=current_user.id,
        page=page,
        size=pageSize.value,
        category=category,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction_by_id(
    transaction_id: uuid.UUID,
    handler: handlers.TransactionHandler = Depends(),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Retrieve a specific transaction by its ID, including product and category details.
    Protected endpoint.
    """
    return handler.get_transaction(transaction_id=transaction_id, user_id=current_user.id)

@router.get("/analytics/amount-per-category", response_model=List[schemas.AmountPerCategory])
def get_spending_by_category(
    handler: handlers.TransactionHandler = Depends(),
    current_user: UserModel = Depends(get_current_user),
    start_date: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)")
):
    """
    Get total amount spent per category for the current user.
    """
    return handler.get_amount_per_category(current_user.id, start_date, end_date)

@router.get("/analytics/count-per-category", response_model=List[schemas.CountPerCategory])
def get_count_by_category(
    handler: handlers.TransactionHandler = Depends(),
    current_user: UserModel = Depends(get_current_user),
    start_date: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)")
):
    """
    Get the count of transactions per category for the current user.
    """
    return handler.get_count_per_category(current_user.id, start_date, end_date)

@router.get("/analytics/time-series", response_model=schemas.TimeSeriesResponse)
def get_spending_time_series(
    handler: handlers.TransactionHandler = Depends(),
    current_user: UserModel = Depends(get_current_user),
    start_date: date = Query(..., description="Start date for the time series (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date for the time series (YYYY-MM-DD)")
):
    """
    Get time series data of transactions (count and amount) for the current user.
    """
    return handler.get_time_series(current_user.id, start_date, end_date)

