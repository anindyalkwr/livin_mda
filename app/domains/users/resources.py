# app/domains/users/resources.py
from sqlalchemy.orm import Session, joinedload
from typing import Optional, Dict, Any

from app.core.security import get_password_hash
from app.database.models import User
from . import schemas

def get_user(db: Session, user_id: str):
    """
    Fetches a single user by their ID, joining with their account details.
    """
    return db.query(User).options(joinedload(User.account)).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Fetches a single user by their email, joining with their account details.
    This is crucial for authentication and for the /users/me endpoint.
    """
    return db.query(User).options(joinedload(User.account)).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> User:
    """
    Creates a new user in the database.
    The associated account is created automatically by a database trigger.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        address=user.address,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_in: schemas.UserUpdate) -> User:
    """
    Updates a user's information.
    """
    update_data = user_in.dict(exclude_unset=True)

    # If a new password is provided, hash it before updating
    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"] # remove plain password
        db_user.hashed_password = hashed_password

    # Update other fields
    for field, value in update_data.items():
        if hasattr(db_user, field):
            setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
