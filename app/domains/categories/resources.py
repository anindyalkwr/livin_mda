from sqlalchemy.orm import Session
from typing import Tuple, List
from app.database.models import Category

def get_all_categories(db: Session, page: int, size: int) -> Tuple[List[Category], int]:
    offset = (page - 1) * size
    query = db.query(Category)
    total = query.count()
    items = query.order_by(Category.label).offset(offset).limit(size).all()
    return items, total