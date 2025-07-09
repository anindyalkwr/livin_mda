from sqlalchemy.orm import Session, joinedload
from typing import Tuple, List, Optional
from app.database.models import Product, Category

def get_all_products(db: Session, page: int, size: int, category_label: Optional[str] = None) -> Tuple[List[Product], int]:
    offset = (page - 1) * size
    query = db.query(Product).options(
        joinedload(Product.category),
        joinedload(Product.merchant)
    )
    
    if category_label:
        query = query.join(Category).filter(Category.label == category_label)

    total = query.count()
    items = query.order_by(Product.name).offset(offset).limit(size).all()
    return items, total