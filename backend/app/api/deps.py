# app/api/deps.py
from typing import Generator, Optional, AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer # Security scheme definition
from jose import jwt, JWTError # Import JWTError for exception handling
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError # For token data validation

from app.core.config import settings
from app.db.session import get_async_db # Import async session getter
# --- UPDATED IMPORTS ---
from app import crud, schemas         # Import crud and schemas as before
from app.db.models.user import User   # Import the User model directly
# -----------------------

# Define the OAuth2 scheme
# tokenUrl should point to your login endpoint
reusable_oauth2 = OAuth2PasswordBearer(
     tokenUrl="/api/v1/login/token"
)

async def get_current_user(
    db: AsyncSession = Depends(get_async_db), token: str = Depends(reusable_oauth2)
) -> User: # <<< Use User type hint directly
    """
    Dependency to get the current user from the JWT token.
    Raises exceptions if token is invalid or user not found.
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Validate the payload structure using Pydantic schema
        # Extract subject (email) from payload
        # --- CORRECTED LINE ---
        token_data = schemas.TokenPayload(**payload) # Use **payload to unpack dict
# --- Make sure you are referencing TokenPayload, not TokenData if you renamed it ---
        if token_data.sub is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials: Subject missing",
            )
    except JWTError as e:
         # Catch specific JWT errors (expired, invalid signature, etc.)
         print(f"JWT Error: {e}") # Log the error for debugging
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials: {e}",
         )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials: Invalid token payload",
         )

    # Get user from database based on subject (email)
    # Reference crud.crud_user correctly
    user = await crud.crud_user.get_user_by_email(db, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user # Returns an instance of the User model

async def get_current_active_user(
    # Use User type hint directly
    current_user: User = Depends(get_current_user),
) -> User: # Use User type hint directly
    """
    Dependency that checks if the user retrieved by get_current_user is active.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Add dependencies for superuser if needed later
# async def get_current_active_superuser(...): ...