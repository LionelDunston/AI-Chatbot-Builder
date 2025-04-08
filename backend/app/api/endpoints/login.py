# app/api/endpoints/login.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Standard form for username/password
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app import schemas, crud
from app.db.session import get_async_db
from app.core import security # Import security utils

router = APIRouter()

@router.post("/login/access-token", response_model=schemas.Token)
async def login_for_access_token(
    # Use OAuth2PasswordRequestForm: requires form data with "username" and "password" keys
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    (Username is the user's email).
    """
    # 1. Authenticate User
    user = await crud.crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}, # Standard header for 401
        )
    elif not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")

    # 2. Create Access Token
    access_token = security.create_access_token(
        subject=user.email # Use email as subject, or user.id
    )

    # 3. Return Token
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }