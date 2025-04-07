# File: backend/app/crud/crud_chatbot.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select # Use select from sqlalchemy.future for 2.0 style queries
from typing import List, Optional

from app.db.models.chatbot import Chatbot # Import the SQLAlchemy model
from app.schemas.chatbot import ChatbotCreate # Import the Pydantic create schema

# --- Create Operation ---
async def create_chatbot(db: AsyncSession, *, chatbot_in: ChatbotCreate, owner_id: int) -> Chatbot:
    """
    Creates a new chatbot record in the database.
    """
    # Create a SQLAlchemy model instance from the Pydantic schema data
    # **chatbot_in.model_dump() unpacks the fields from the Pydantic model
    db_chatbot = Chatbot(**chatbot_in.model_dump(), owner_id=owner_id)

    # Add the new chatbot instance to the session
    db.add(db_chatbot)

    # Commit the changes to the database
    await db.commit()

    # Refresh the instance to get any database-generated values (like ID, created_at)
    await db.refresh(db_chatbot)

    return db_chatbot # Return the newly created chatbot object

# --- Read Operations ---
async def get_chatbot(db: AsyncSession, chatbot_id: int) -> Optional[Chatbot]:
    """
    Retrieves a single chatbot by its ID.
    """
    # Asynchronously execute a select statement to get the chatbot by primary key
    result = await db.execute(select(Chatbot).filter(Chatbot.id == chatbot_id))
    return result.scalar_one_or_none() # Return the single result or None if not found

async def get_chatbots_by_owner(db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100) -> List[Chatbot]:
    """
    Retrieves a list of chatbots owned by a specific user, with pagination.
    """
    # Asynchronously execute a select statement
    result = await db.execute(
        select(Chatbot)
        .filter(Chatbot.owner_id == owner_id) # Filter by owner
        .order_by(Chatbot.created_at.desc()) # Order by creation date (newest first)
        .offset(skip) # Skip records for pagination
        .limit(limit) # Limit the number of records returned
    )
    return result.scalars().all() # Return all matching chatbot objects as a list

# --- Update Operation --- (We'll implement this later)
# async def update_chatbot(db: AsyncSession, *, db_chatbot: Chatbot, chatbot_in: ChatbotUpdate) -> Chatbot:
#     ...

# --- Delete Operation --- (We'll implement this later)
# async def remove_chatbot(db: AsyncSession, *, chatbot_id: int) -> Optional[Chatbot]:
#     ...