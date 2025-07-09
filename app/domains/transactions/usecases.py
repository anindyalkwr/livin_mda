from sqlalchemy.orm import Session
import uuid
from typing import Optional
from datetime import date
from . import schemas, resources

class TransactionUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute_deposit(self, user_id: uuid.UUID, deposit: schemas.DepositCreate):
        return resources.create_deposit(self.db, user_id=user_id, deposit=deposit)

    def execute_payment(self, user_id: uuid.UUID, payment: schemas.PaymentCreate):
        return resources.create_payment(self.db, user_id=user_id, payment=payment)

    def get_transaction_details(self, transaction_id: uuid.UUID, user_id: uuid.UUID):
        return resources.get_transaction_by_id(self.db, transaction_id=transaction_id, user_id=user_id)

    def list_user_transactions(
        self,
        user_id: uuid.UUID,
        page: int,
        size: int,
        category: Optional[str],
        start_date: Optional[date],
        end_date: Optional[date]
    ):
        return resources.get_user_transactions(
            self.db,
            user_id=user_id,
            page=page,
            size=size,
            category_label=category,
            start_date=start_date,
            end_date=end_date
        )
    
    def get_spending_by_category(self, user_id: uuid.UUID, start_date: Optional[date], end_date: Optional[date]):
        return resources.get_amount_per_category(self.db, user_id, start_date, end_date)

    def get_count_by_category(self, user_id: uuid.UUID, start_date: Optional[date], end_date: Optional[date]):
        return resources.get_count_per_category(self.db, user_id, start_date, end_date)

    def get_spending_time_series(self, user_id: uuid.UUID, start_date: date, end_date: date):
        return resources.get_time_series_data(self.db, user_id, start_date, end_date)