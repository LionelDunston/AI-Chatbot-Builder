# app/crud/crud_chatbot.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update # If needed for update later
from app.db.models.chatbot import Chatbot, ChatbotStatus # Import DB model and Enum
from app.schemas.chatbot import ChatbotCreate # Import Pydantic schema
from typing import List

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

# Example for later (Update status)
# async def update_chatbot_status(db: AsyncSession, chatbot_id: int, status: ChatbotStatus) -> Chatbot | None:
#    await db.execute(
#        update(Chatbot)
#        .where(Chatbot.id == chatbot_id)
#        .values(status=status)
#    )
#    await db.commit()
#    return await get_chatbot(db, chatbot_id) # Return updated chatbot