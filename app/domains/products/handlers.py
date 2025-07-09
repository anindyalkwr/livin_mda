from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional
from app.database.connection import get_db
from . import usecases, schemas

def get_product_usecase(db: Session = Depends(get_db)) -> usecases.ProductUseCase:
    return usecases.ProductUseCase(db)

class ProductHandler:
    def __init__(self, usecase: usecases.ProductUseCase = Depends(get_product_usecase)):
        self.usecase = usecase

    def get_all_products(self, page: int, size: int, category: Optional[str]):
        items, total = self.usecase.list_all_products(page, size, category)
        return schemas.ProductList(items=items, total=total, page=page, size=size)