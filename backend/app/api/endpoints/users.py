# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any # Use Any for now, or List[schemas.UserRead] later

from app.schemas.user import UserCreate, UserRead # Use __init__.py for easier imports if preferred
from app import crud
from app.db.session import get_async_db

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    *,
    db: AsyncSession = Depends(get_async_db),
    user_in: UserCreate # Direct usage
) -> Any: # Return type hint
    """
    Create new user.
    """
    # Check if user already exists
    existing_user = await crud.crud_user.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    # Create the user using the CRUD function
    user = await crud.crud_user.create_user(db=db, user_in=user_in)
    return user # FastAPI automatically converts DB model to response_model

@router.get("/{user_id}", response_model=UserRead)
async def read_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await crud.crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist",
        )
    return user