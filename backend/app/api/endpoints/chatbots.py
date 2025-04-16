# app/api/endpoints/chatbots.py
from app.api import deps
from app.db import models
from ...db.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List

from app import schemas
from app import crud
from app.db.session import get_async_db

from app.schemas.chatbot import ChatbotCreate, ChatbotRead # Import directly
from app.schemas.user import UserRead # Need this if you add user info later


router = APIRouter()

@router.post("/", response_model=schemas.ChatbotRead, status_code=status.HTTP_201_CREATED)
async def create_new_chatbot(
    *,
    db: AsyncSession = Depends(get_async_db),
    chatbot_in: schemas.ChatbotCreate,
    # --- REPLACE hardcoded owner_id with dependency ---
    # owner_id: int = 1 # <<< REMOVE THIS
    current_user: models.User = Depends(deps.get_current_active_user) # <<< ADD THIS
    # --------------------------------------------------
) -> Any:
    """
    Create new chatbot. Requires authentication.
    """
    # --- Use the authenticated user's ID ---
    chatbot = await crud.crud_chatbot.create_chatbot(
        db=db, chatbot_in=chatbot_in, owner_id=current_user.id # <<< USE THIS
    )
    # ----------------------------------------
    return chatbot

# --- Optionally protect other chatbot endpoints similarly ---
@router.get("/{chatbot_id}", response_model=schemas.ChatbotRead)
async def read_chatbot_by_id(
    chatbot_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(deps.get_current_active_user) # <<< ADD protection
) -> Any:
    chatbot = await crud.crud_chatbot.get_chatbot(db, chatbot_id=chatbot_id)
    if not chatbot:
         raise HTTPException(status_code=404, detail="Chatbot not found")
    # --- Add ownership check ---
    if chatbot.owner_id != current_user.id and not current_user.is_superuser:
         raise HTTPException(status_code=403, detail="Not enough permissions")
    # -------------------------
    return chatbot

@router.get("/my/", response_model=List[schemas.ChatbotRead])
async def read_my_chatbots(
    db: AsyncSession = Depends(get_async_db),
    # --- REPLACE hardcoded owner_id ---
    # owner_id: int = 1, # <<< REMOVE
    current_user: models.User = Depends(deps.get_current_active_user), # <<< ADD
    # --------------------------------
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve chatbots owned by the current authenticated user.
    """
    # --- Use authenticated user's ID ---
    chatbots = await crud.crud_chatbot.get_chatbots_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit # <<< USE THIS
    )
    # -----------------------------------
    return chatbots

# --- NEW ENDPOINT: Update Chatbot ---
@router.patch("/{chatbot_id}", response_model=schemas.ChatbotRead)
async def update_existing_chatbot(
    *,
    db: AsyncSession = Depends(get_async_db),
    chatbot_id: int,
    chatbot_in: schemas.ChatbotUpdate, # Request body with optional fields
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Update a chatbot owned by the current user.
    """
    updated_chatbot = await crud.crud_chatbot.update_chatbot(
        db=db,
        chatbot_id=chatbot_id,
        chatbot_in=chatbot_in,
        owner_id=current_user.id # Pass owner ID for check in CRUD
    )

    # CRUD function returns None if not found or not owned
    if not updated_chatbot:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found or not authorized to update",
         )

    return updated_chatbot
# ----------------------------------

# --- NEW ENDPOINT: Delete Chatbot ---
@router.delete("/{chatbot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_chatbot(
    *,
    db: AsyncSession = Depends(get_async_db),
    chatbot_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> None: # Returns None on success (204 No Content)
    """
    Delete a chatbot owned by the current user.
    """
    deleted = await crud.crud_chatbot.delete_chatbot(
        db=db,
        chatbot_id=chatbot_id,
        owner_id=current_user.id # Pass owner ID for check in CRUD
    )

    # CRUD function returns False if not found or not owned
    if not deleted:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found or not authorized to delete",
         )

    # No content to return on successful delete
    return None