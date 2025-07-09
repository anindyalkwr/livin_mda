import uuid
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from . import handlers, schemas
from app.core.security import create_access_token, verify_password
from app.core.config import settings
from app.middleware.auth import get_current_user
from app.database.models import User as UserModel # Import the ORM model

router = APIRouter()

# --- Public Endpoints ---

@router.post("/users/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user_registration(
    user_in: schemas.UserCreate,
    handler: handlers.UserHandler = Depends()
):
    """
    Create new user. Publicly accessible.
    """
    return handler.register_user(user_in)

@router.post("/users/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    handler: handlers.UserHandler = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    Username field should contain the user's email.
    """
    user = handler.get_user_for_auth(email=form_data.username)
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Protected Endpoints ---

@router.get("/users/me", response_model=schemas.User)
def read_current_user(current_user: UserModel = Depends(get_current_user)):
    """
    Get current logged-in user's details, including their account balance.
    This endpoint is protected.
    """
    return current_user

@router.put("/users/me", response_model=schemas.User)
def update_current_user(
    user_in: schemas.UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    handler: handlers.UserHandler = Depends()
):
    """
    Update current user's details (full name, address, email, password).
    This endpoint is protected.
    """
    return handler.update_user(user_to_update=current_user, update_data=user_in)
