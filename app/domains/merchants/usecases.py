from sqlalchemy.orm import Session
from . import resources

class MerchantUseCase:
    def __init__(self, db: Session):
        self.db = db
    
    def list_all_merchants(self, page: int, size: int):
        return resources.get_all_merchants(self.db, page, size)