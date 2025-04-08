# backend/app/main.py
from fastapi import FastAPI
from app.api.endpoints import users, chatbots
# --- REMOVED unused imports ---
# from app.db.session import engine  # REMOVED
# from app.db.base import Base       # Remove if Base is also not used directly here
# -----------------------------
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Chatbot Builder API",
    description="API for creating and managing AI chatbots.",
    version="0.1.0"
)

# --- INCLUDE ROUTERS ---
api_prefix = "/api/v1"
app.include_router(users.router, prefix=f"{api_prefix}/users", tags=["users"])
app.include_router(chatbots.router, prefix=f"{api_prefix}/chatbots", tags=["chatbots"])
# -----------------------

@app.get("/")
async def read_root():
    return {"message": f"Welcome to {app.title} v{app.version}"}