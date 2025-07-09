from sqlalchemy.orm import Session
from . import schemas, resources

class UserUseCase:
    def __init__(self, db: Session):
        self.db = db

    def create_new_user(self, user: schemas.UserCreate):
        db_user = resources.get_user_by_email(self.db, email=user.email)
        if db_user:
            return None
        return resources.create_user(self.db, user=user)

    def find_user_by_email(self, email: str):
        return resources.get_user_by_email(self.db, email=email)

    def update_user_details(self, user_to_update: schemas.User, update_data: schemas.UserUpdate):
        return resources.update_user(self.db, db_user=user_to_update, user_in=update_data)