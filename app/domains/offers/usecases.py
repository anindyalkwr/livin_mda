from sqlalchemy.orm import Session
from typing import Optional
from . import resources

class OfferUseCase:
    def __init__(self, db: Session):
        self.db = db
    
    def list_all_offers(self, page: int, size: int, category: Optional[str]):
        return resources.get_all_offers(self.db, page, size, category_label=category)