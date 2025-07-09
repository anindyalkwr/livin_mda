from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from app.database.connection import get_db
from . import usecases, schemas

def get_offer_usecase(db: Session = Depends(get_db)) -> usecases.OfferUseCase:
    return usecases.OfferUseCase(db)

class OfferHandler:
    def __init__(self, usecase: usecases.OfferUseCase = Depends(get_offer_usecase)):
        self.usecase = usecase

    def get_all_offers(self, page: int, size: int, category: Optional[str]):
        items, total = self.usecase.list_all_offers(page, size, category)
        return schemas.OfferList(items=items, total=total, page=page, size=size)
