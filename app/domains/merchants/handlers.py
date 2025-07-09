from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.connection import get_db
from . import usecases, schemas

def get_merchant_usecase(db: Session = Depends(get_db)) -> usecases.MerchantUseCase:
    return usecases.MerchantUseCase(db)

class MerchantHandler:
    def __init__(self, usecase: usecases.MerchantUseCase = Depends(get_merchant_usecase)):
        self.usecase = usecase

    def get_all_merchants(self, page: int, size: int):
        items, total = self.usecase.list_all_merchants(page, size)
        return schemas.MerchantList(items=items, total=total, page=page, size=size)
