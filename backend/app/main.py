# File: backend/app/main.py
from fastapi import FastAPI
# We will import and include routers here later
# from app.api.api import api_router
# from app.core.config import settings

# Create the main FastAPI application instance
app = FastAPI(
    title="AI Chatbot Builder API",
    description="API for creating and managing AI chatbots.",
    version="0.1.0",
    # Add other metadata if desired
    # openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Later, we will include routers like this:
# app.include_router(api_router, prefix="/api/v1") # Example prefix

# Simple root endpoint to check if the API is running
@app.get("/")
async def root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to AI Chatbot Builder API v0.1.0"}

# Add application event handlers if needed (e.g., startup/shutdown)
# @app.on_event("startup")
# async def startup_event():
#     print("Application starting up...")
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Application shutting down...")