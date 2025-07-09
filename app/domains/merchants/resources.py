from sqlalchemy.orm import Session
from typing import Tuple, List
from app.database.models import Merchant

def get_all_merchants(db: Session, page: int, size: int) -> Tuple[List[Merchant], int]:
    offset = (page - 1) * size
    query = db.query(Merchant)
    total = query.count()
    items = query.order_by(Merchant.name).offset(offset).limit(size).all()
    return items, total