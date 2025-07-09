from sqlalchemy.orm import Session, joinedload
from typing import Tuple, List, Optional
from app.database.models import Offer, Category

def get_all_offers(db: Session, page: int, size: int, category_label: Optional[str] = None) -> Tuple[List[Offer], int]:
    offset = (page - 1) * size
    query = db.query(Offer).options(joinedload(Offer.category))

    if category_label:
        query = query.join(Category).filter(Category.label == category_label)

    total = query.count()
    items = query.order_by(Offer.name).offset(offset).limit(size).all()
    return items, total