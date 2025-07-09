from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.connection import get_db
from . import usecases, schemas

def get_category_usecase(db: Session = Depends(get_db)) -> usecases.CategoryUseCase:
    return usecases.CategoryUseCase(db)

class CategoryHandler:
    def __init__(self, usecase: usecases.CategoryUseCase = Depends(get_category_usecase)):
        self.usecase = usecase

    def get_all_categories(self, page: int, size: int):
        items, total = self.usecase.list_all_categories(page, size)
        return schemas.CategoryList(items=items, total=total, page=page, size=size)
