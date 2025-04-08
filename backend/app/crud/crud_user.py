# app/crud/crud_user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User # Import DB model
from app.schemas.user import UserCreate # Import Pydantic schema
from app.core.security import get_password_hash # Import hashing function

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    """Gets a single user by ID."""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Gets a single user by email."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, *, user_in: UserCreate) -> User:
    """Creates a new user."""
    hashed_password = get_password_hash(user_in.password)
    # Create a User model instance (DB model)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password
        # is_active and is_superuser use defaults from the model
    )
    db.add(db_user) # Add instance to the session
    await db.commit() # Commit the transaction
    await db.refresh(db_user) # Refresh instance to get DB-generated data (like ID)
    return db_user