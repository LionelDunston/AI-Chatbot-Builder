# backend/app/api/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List # Added List for potential future use

# Import schemas defined in app/schemas/
from app.schemas.user import UserCreate, UserRead

# Import CRUD functions
from app import crud

# Import dependency utilities from app/api/deps.py
from app.api import deps

# Import the async database session dependency
from app.db.session import get_async_db

# Import the database model for type hinting the current_user dependency
from app.db.models.user import User

# Create an API router instance
router = APIRouter()


# --- Endpoint to Get Current Logged-in User ---
@router.get("/me", response_model=UserRead)
async def read_users_me(
    # Use the dependency function from deps.py to get the validated, active user
    # The dependency handles token extraction, validation, and user lookup
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get profile for the currently logged-in user.
    Requires authentication token in the header.
    """
    # The dependency `get_current_active_user` already returns the User DB model object.
    # FastAPI, using the `response_model=UserRead`, will automatically convert
    # the User DB model attributes into the UserRead Pydantic schema format for the response.
    return current_user


# --- Endpoint to Create a New User ---
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    *, # Make subsequent arguments keyword-only
    db: AsyncSession = Depends(get_async_db), # Inject DB session
    user_in: UserCreate # Request body validated against UserCreate schema
) -> Any:
    """
    Create a new user account.
    Validates input email and password, checks for existing user,
    hashes the password, and saves to the database.
    """
    # Check if a user with the given email already exists
    existing_user = await crud.crud_user.get_user_by_email(db, email=user_in.email)
    if existing_user:
        # If user exists, raise an HTTP exception (400 Bad Request)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    # If user doesn't exist, call the CRUD function to create the user
    # The CRUD function handles password hashing internally
    user = await crud.crud_user.create_user(db=db, user_in=user_in)

    # Return the created user object (will be serialized according to UserRead schema)
    return user


# --- Endpoint to Get a Specific User by ID ---
@router.get("/{user_id}", response_model=UserRead)
async def read_user_by_id(
    user_id: int, # Path parameter for the user ID
    db: AsyncSession = Depends(get_async_db), # Inject DB session
    # Optional: Add dependency check for permissions later
    # current_user: User = Depends(deps.get_current_active_superuser) # Example
) -> Any:
    """
    Get details for a specific user by their ID.
    (Currently accessible by anyone, consider adding permission checks).
    """
    # Call the CRUD function to fetch the user by ID
    user = await crud.crud_user.get_user(db, user_id=user_id)

    # If the user is not found in the database, raise HTTP 404 Not Found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist",
        )

    # Return the found user object (serialized as UserRead)
    return user

# Potential future endpoints to add here:
# - GET / : List users (likely requires admin privileges)
# - PUT/PATCH /{user_id} : Update a user (requires permissions)
# - DELETE /{user_id} : Delete a user (requires permissions)