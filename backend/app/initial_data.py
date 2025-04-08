# backend/app/initial_data.py
import logging
import asyncio

# --- Import the ASYNC engine ---
from app.db.session import async_engine

# --- STEP 1: Import Base DIRECTLY from its definition ---
from app.db.models.base_class import Base
# --- DO NOT import from app.db.base here ---

# --- STEP 2: Import the models HERE to register them with the imported Base ---
from app.db.models.user import User
from app.db.models.chatbot import Chatbot
# --- Import other models if needed ---


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    logger.info("Creating initial database tables (async - direct model import)...")
    # --- Log metadata state BEFORE creating tables ---
    # This check uses the Base imported directly above, after model imports
    logger.info(f"Base metadata tables BEFORE create: {Base.metadata.tables.keys()}")
    # -------------------------------------------------------

    if not Base.metadata.tables:
         logger.error("FATAL: No tables found in Base metadata even after direct model imports!")
         await async_engine.dispose()
         return # Exit

    try:
        async with async_engine.begin() as conn:
             # run_sync uses the Base.metadata object, populated by the direct model imports
             await conn.run_sync(Base.metadata.create_all)
        # --- Log metadata state AFTER creating tables ---
        logger.info(f"Base metadata tables AFTER create: {Base.metadata.tables.keys()}")
        # ------------------------------------------------------
        logger.info("Database tables created successfully (async - direct model import).")
    except Exception as e:
        logger.error(f"Error creating database tables (async): {e}")
        # --- Log metadata state on error ---
        logger.error(f"Base metadata tables during error: {Base.metadata.tables.keys()}")
        # ---------------------------------
        raise
    finally:
         # Gracefully close the engine connections
         await async_engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())