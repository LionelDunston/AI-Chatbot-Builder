# backend/app/main.py
import logging
from fastapi import FastAPI

# --- Explicitly import the ROUTER from each specific endpoint module ---
# These are the modules you DO have:
from app.api.endpoints.users import router as users_router
from app.api.endpoints.chatbots import router as chatbots_router
from app.api.endpoints.login import router as login_router
from app.api.endpoints.data_sources import router as data_sources_router
# --- Removed import for items ---

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="AI Chatbot Builder API",
    description="API for creating and managing AI chatbots.",
    version="0.1.0",
)

# Define a common prefix for API versioning
api_prefix = "/api/v1"

# --- Include Routers using the imported router variables ---
app.include_router(
    login_router,
    prefix=f"{api_prefix}/login", # Ensure tokenUrl in deps.py matches this!
    tags=["login"]
)
app.include_router(
    users_router,
    prefix=f"{api_prefix}/users",
    tags=["users"]
)
app.include_router(
    chatbots_router,
    prefix=f"{api_prefix}/chatbots",
    tags=["chatbots"]
)
app.include_router(
    data_sources_router,
    prefix=f"{api_prefix}/chatbots", # Mounts relative to chatbots (e.g., /chatbots/{id}/upload-file)
    tags=["data_sources"]
)
# --- Removed include_router for items ---

# Root endpoint
@app.get("/")
async def read_root():
    """Provides a simple welcome message indicating the API is running."""
    return {"message": f"Welcome to {app.title} v{app.version}"}