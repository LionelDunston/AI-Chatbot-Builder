# File: backend/app/api/api.py
from fastapi import APIRouter

# Import the chatbots module itself from the endpoints package
from app.api.endpoints import chatbots

# Create the main API router
api_router = APIRouter()

# Include the 'router' object that is defined INSIDE the imported 'chatbots' module
# We access it using dot notation: chatbots.router
api_router.include_router(chatbots.router)

# Include other routers here later (e.g., for users, auth, data sources)
# from app.api.endpoints import users, auth
# api_router.include_router(users.router)
# api_router.include_router(auth.router)