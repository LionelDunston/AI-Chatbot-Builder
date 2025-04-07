# File: backend/app/api/endpoints/chatbots.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# NEW IMPORTS (Using relative paths):
from ...db.base import get_db # Go up 3 levels for db
from ...schemas.chatbot import Chatbot, ChatbotCreate # Go up 3 levels for schemas
from ...crud import crud_chatbot # Go up 3 levels for crud

# Create an APIRouter instance
# Tags are used for grouping endpoints in the OpenAPI documentation
router = APIRouter(prefix="/chatbots", tags=["Chatbots"])

@router.post("/", response_model=Chatbot, status_code=status.HTTP_201_CREATED)
async def create_new_chatbot(
    *,
    db: AsyncSession = Depends(get_db), # Inject DB session
    chatbot_in: ChatbotCreate # Request body based on Pydantic schema
    # current_user: models.User = Depends(get_current_active_user) # We'll add this later for auth
):
    """
    Create a new chatbot.
    (Currently uses a placeholder owner_id=1)
    """
    # TODO: Replace placeholder owner_id with ID from authenticated user
    placeholder_owner_id = 1
    # We need a user to exist in the DB first for this to work!
    # We will add user creation/auth later. For now, manually create user 1 if needed.

    try:
        chatbot = await crud_chatbot.create_chatbot(db=db, chatbot_in=chatbot_in, owner_id=placeholder_owner_id)
        return chatbot
    except Exception as e:
        # Basic error handling for now
        # In a real app, you might check for specific DB errors (e.g., user not found)
        print(f"Error creating chatbot: {e}") # Log the error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create chatbot.",
        )


@router.get("/", response_model=List[Chatbot])
async def read_chatbots_for_owner(
    db: AsyncSession = Depends(get_db), # Inject DB session
    skip: int = 0, # Query parameter for pagination offset
    limit: int = 100 # Query parameter for pagination limit
    # current_user: models.User = Depends(get_current_active_user) # Will use later for auth
):
    """
    Retrieve chatbots owned by the current user.
    (Currently uses placeholder owner_id=1)
    """
     # TODO: Replace placeholder owner_id with ID from authenticated user
    placeholder_owner_id = 1

    chatbots = await crud_chatbot.get_chatbots_by_owner(db=db, owner_id=placeholder_owner_id, skip=skip, limit=limit)
    return chatbots


@router.get("/{chatbot_id}", response_model=Chatbot)
async def read_chatbot(
    chatbot_id: int, # Path parameter from the URL
    db: AsyncSession = Depends(get_db)
    # current_user: models.User = Depends(get_current_active_user) # Will use later for auth & ownership check
):
    """
    Retrieve a specific chatbot by its ID.
    """
    db_chatbot = await crud_chatbot.get_chatbot(db=db, chatbot_id=chatbot_id)
    if db_chatbot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chatbot not found")

    # TODO: Add check here later to ensure the current_user owns this chatbot
    # if db_chatbot.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this chatbot")

    return db_chatbot

# Add endpoints for Update and Delete later
# @router.put("/{chatbot_id}", ...)
# async def update_existing_chatbot(...): ...
#
# @router.delete("/{chatbot_id}", ...)
# async def delete_existing_chatbot(...): ...