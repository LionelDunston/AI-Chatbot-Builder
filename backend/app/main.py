# app/main.py
from fastapi import FastAPI
# --- UPDATED IMPORTS ---
from app.api.endpoints import  users_router
from app.api.endpoints import  chatbots_router
from app.api.endpoints import  login_router
# -----------------------
# from app.db.session import engine # Usually not needed directly here anymore
# from app.db.base import Base      # Usually not needed directly here anymore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Chatbot Builder API",
    description="API for creating and managing AI chatbots.",
    version="0.1.0" # Good practice to add versioning
)

# --- INCLUDE ROUTERS USING ALIASES ---
# Use tags for grouping in documentation
api_prefix = "/api/v1"
# Include login router (adjust prefix if needed, e.g., just /api)
app.include_router(login_router, prefix="/api", tags=["login"])
# Include other routers with v1 prefix
app.include_router(users_router, prefix=f"{api_prefix}/users", tags=["users"])
app.include_router(chatbots_router, prefix=f"{api_prefix}/chatbots", tags=["chatbots"])
 # Keep example if desired
# -------------------------------------

@app.get("/")
async def read_root():
     # Update root message if desired
     return {"message": f"Welcome to {app.title} v{app.version}"}

# Any other app setup (middleware, exception handlers) would go here