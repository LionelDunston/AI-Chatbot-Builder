# app/crud/crud_chatbot.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update # If needed for update later
from app.db.models.chatbot import Chatbot, ChatbotStatus # Import DB model and Enum
from app.schemas.chatbot import ChatbotCreate # Import Pydantic schema
from typing import List
from app.schemas.chatbot import ChatbotUpdate

async def get_chatbot(db: AsyncSession, chatbot_id: int) -> Chatbot | None:
    """Gets a single chatbot by ID."""
    result = await db.execute(select(Chatbot).filter(Chatbot.id == chatbot_id))
    
    return result.scalars().first()

async def get_chatbots_by_owner(db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Chatbot]:
    """Gets a list of chatbots for a specific owner."""
    result = await db.execute(
        select(Chatbot)
        .filter(Chatbot.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_chatbot(db: AsyncSession, *, chatbot_in: ChatbotCreate, owner_id: int) -> Chatbot:
    """Creates a new chatbot."""
    db_chatbot = Chatbot(
        name=chatbot_in.name,
        owner_id=owner_id
        # status uses default PENDING from the model
        # created_at/updated_at use server defaults
    )
    db.add(db_chatbot)
    await db.commit()
    await db.refresh(db_chatbot)
    return db_chatbot

# --- NEW FUNCTION: Update Chatbot ---
async def update_chatbot(
    db: AsyncSession, *, chatbot_id: int, chatbot_in: ChatbotUpdate, owner_id: int
) -> Chatbot | None:
    """
    Updates a chatbot. Ensures the user owns the chatbot.
    Returns the updated chatbot object or None if not found or not owned.
    """
    # First, get the existing chatbot
    db_chatbot = await get_chatbot(db=db, chatbot_id=chatbot_id)

    # Check if chatbot exists and if the user owns it
    if not db_chatbot or db_chatbot.owner_id != owner_id:
        return None # Indicate not found or not authorized

    # Get the update data from the input schema
    update_data = chatbot_in.model_dump(exclude_unset=True) # Get only fields that were provided

    # Update the chatbot object in memory
    needs_update = False
    for field, value in update_data.items():
        if hasattr(db_chatbot, field) and value is not None:
             setattr(db_chatbot, field, value)
             needs_update = True

    # Only commit if there were actual changes
    if needs_update:
        # Manually set updated_at if needed, or rely on DB trigger if set up
        # db_chatbot.updated_at = datetime.datetime.now(datetime.timezone.utc)
        db.add(db_chatbot) # Add tracked object back to session (though often tracked already)
        await db.commit()
        await db.refresh(db_chatbot)

    return db_chatbot
# ------------------------------------

# --- NEW FUNCTION: Delete Chatbot ---
async def delete_chatbot(db: AsyncSession, *, chatbot_id: int, owner_id: int) -> bool:
    """
    Deletes a chatbot. Ensures the user owns the chatbot.
    Returns True if deleted, False otherwise (not found or not owned).
    """
    # First, get the existing chatbot to verify ownership
    db_chatbot = await get_chatbot(db=db, chatbot_id=chatbot_id)

    # Check if chatbot exists and if the user owns it
    if not db_chatbot or db_chatbot.owner_id != owner_id:
        return False # Indicate not found or not authorized

    # If checks pass, proceed with deletion
    await db.delete(db_chatbot) # Mark the object for deletion
    await db.commit()           # Commit the transaction
    return True                 # Indicate successful deletion
# ----------------------------------