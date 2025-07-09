from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
import uuid
from typing import Optional, List
from datetime import date
from app.database.connection import get_db
from . import usecases, schemas

def get_transaction_usecase(db: Session = Depends(get_db)) -> usecases.TransactionUseCase:
    return usecases.TransactionUseCase(db)

class TransactionHandler:
    def __init__(self, usecase: usecases.TransactionUseCase = Depends(get_transaction_usecase)):
        self.usecase = usecase

    def process_deposit(self, user_id: uuid.UUID, deposit: schemas.DepositCreate):
        try:
            return self.usecase.execute_deposit(user_id, deposit)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def process_payment(self, user_id: uuid.UUID, payment: schemas.PaymentCreate):
        transaction, error_msg = self.usecase.execute_payment(user_id, payment)
        if error_msg:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
        return transaction

    def get_transaction(self, transaction_id: uuid.UUID, user_id: uuid.UUID):
        transaction = self.usecase.get_transaction_details(transaction_id, user_id)
        if not transaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
        return transaction

    def get_my_transactions(
        self, user_id: uuid.UUID, page: int, size: int,
        category: Optional[str], start_date: Optional[date], end_date: Optional[date]
    ):
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
        
        items, total = self.usecase.list_user_transactions(user_id, page, size, category, start_date, end_date)
        return schemas.TransactionHistory(items=items, total=total, page=page, size=size)

    def get_amount_per_category(self, user_id: uuid.UUID, start_date: Optional[date], end_date: Optional[date]) -> List[schemas.AmountPerCategory]:
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
        
        results = self.usecase.get_spending_by_category(user_id, start_date, end_date)
        return [schemas.AmountPerCategory(category=cat, total_amount=amount) for cat, amount in results]

    def get_count_per_category(self, user_id: uuid.UUID, start_date: Optional[date], end_date: Optional[date]) -> List[schemas.CountPerCategory]:
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
        
        results = self.usecase.get_count_by_category(user_id, start_date, end_date)
        return [schemas.CountPerCategory(category=cat, transaction_count=count) for cat, count in results]

    def get_time_series(self, user_id: uuid.UUID, start_date: date, end_date: date) -> schemas.TimeSeriesResponse:
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
        
        results = self.usecase.get_spending_time_series(user_id, start_date, end_date)
        data_points = [schemas.TimeSeriesDataPoint(date=d, transaction_count=c, total_amount=a) for d, c, a in results]
        return schemas.TimeSeriesResponse(data=data_points)
