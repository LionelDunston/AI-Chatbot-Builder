# File: backend/app/main.py
from fastapi import FastAPI
from app.api.api import api_router # <--- IMPORT the main api_router
# from app.core.config import settings

# Create the main FastAPI application instance
app = FastAPI(
    title="AI Chatbot Builder API",
    description="API for creating and managing AI chatbots.",
    version="0.1.0",
)

# --- INCLUDE THE API ROUTER ---
# All routes defined in api_router (which includes chatbots.router)
# will be added to the main app instance.
# We can add a prefix like /api/v1 if desired
app.include_router(api_router, prefix="/api/v1")
# -----------------------------

# Simple root endpoint (optional, can be removed if prefixing everything)
@app.get("/")
async def root():
    # CORRECTED MESSAGE: Point to /docs, not /api/v1/docs
    return {"message": "Welcome to AI Chatbot Builder API v0.1.0 - Use /docs for API documentation."}

# @app.on_event("startup")
# async def startup_event(): ...
#
# @app.on_event("shutdown")
# async def shutdown_event(): ...