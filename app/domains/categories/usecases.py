from sqlalchemy.orm import Session
from . import resources

class CategoryUseCase:
    def __init__(self, db: Session):
        self.db = db
    
    def list_all_categories(self, page: int, size: int):
        return resources.get_all_categories(self.db, page, size)