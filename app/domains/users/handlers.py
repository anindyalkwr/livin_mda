# app/domains/users/handlers.py
import re
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.database.connection import get_db
from app.database.models import User as UserModel
from . import usecases, schemas

def get_user_usecase(db: Session = Depends(get_db)) -> usecases.UserUseCase:
    return usecases.UserUseCase(db)

class UserHandler:
    def __init__(self, usecase: usecases.UserUseCase = Depends(get_user_usecase)):
        self.usecase = usecase

    def _validate_email(self, email: str):
        """
        Validates the email format using a regex.
        Raises HTTPException if validation fails.
        """
        EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(EMAIL_PATTERN, email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The provided email address is not a valid format."
            )

    def _validate_password(self, password: str):
        """
        Validates the password against the required regex.
        Raises HTTPException if validation fails.
        """
        PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(PASSWORD_PATTERN, password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character."
            )

    def register_user(self, user: schemas.UserCreate):
        self._validate_email(user.email)
        self._validate_password(user.password)
        
        new_user = self.usecase.create_new_user(user)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system.",
            )
        return new_user

    def get_user_for_auth(self, email: str):
        user = self.usecase.find_user_by_email(email=email)
        if not user:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def update_user(self, user_to_update: UserModel, update_data: schemas.UserUpdate):
        if update_data.email and update_data.email != user_to_update.email:
            self._validate_email(update_data.email)
            existing_user = self.usecase.find_user_by_email(email=update_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="An account with this email already exists.",
                )
        
        if update_data.password:
            self._validate_password(update_data.password)

        return self.usecase.update_user_details(user_to_update, update_data)
