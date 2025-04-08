# app/api/endpoints/chatbots.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List

from app import schemas
from app import crud
from app.db.session import get_async_db

from app.schemas.chatbot import ChatbotCreate, ChatbotRead # Import directly
from app.schemas.user import UserRead # Need this if you add user info later


router = APIRouter()

@router.post("/", response_model=ChatbotRead, status_code=status.HTTP_201_CREATED)
async def create_new_chatbot(
    *,
    db: AsyncSession = Depends(get_async_db),
    chatbot_in: schemas.ChatbotCreate,
    # --- IMPORTANT: Handle Owner ID ---
    # Option 1: Hardcode for now (requires user ID 1 to exist)
    owner_id: int = 1 # <<< TEMPORARY - REPLACE WITH AUTHENTICATION LATER
    # Option 2: Add dependency for current user (Requires Authentication setup first)
    # current_user: models.User = Depends(get_current_active_user) # <<< FUTURE
) -> Any:
    """
    Create new chatbot. Requires owner_id (currently hardcoded).
    """
    # In future, use current_user.id instead of hardcoded owner_id
    chatbot = await crud.crud_chatbot.create_chatbot(
        db=db, chatbot_in=chatbot_in, owner_id=owner_id # Use hardcoded ID for now
    )
    return chatbot

@router.get("/{chatbot_id}", response_model=ChatbotRead)
async def read_chatbot_by_id(
    chatbot_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> Any:
    """
    Get a specific chatbot by id.
    """
    chatbot = await crud.crud_chatbot.get_chatbot(db, chatbot_id=chatbot_id)
    if not chatbot:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The chatbot with this id does not exist",
        )
    # TODO: Add check later to ensure the current user owns this chatbot
    return chatbot

# Example: Get chatbots for the (currently hardcoded) owner
@router.get("/my/", response_model=List[ChatbotRead])
async def read_my_chatbots(
    db: AsyncSession = Depends(get_async_db),
    # --- IMPORTANT: Handle Owner ID ---
    owner_id: int = 1, # <<< TEMPORARY
    # current_user: models.User = Depends(get_current_active_user), # <<< FUTURE
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve chatbots owned by the user (currently hardcoded user 1).
    """
    chatbots = await crud.crud_chatbot.get_chatbots_by_owner(
        db=db, owner_id=owner_id, skip=skip, limit=limit # Use hardcoded ID for now
    )
    return chatbots