from sqlalchemy.orm import Session
from typing import Optional
from . import resources

class ProductUseCase:
    def __init__(self, db: Session):
        self.db = db
    
    def list_all_products(self, page: int, size: int, category: Optional[str]):
        return resources.get_all_products(self.db, page, size, category_label=category)