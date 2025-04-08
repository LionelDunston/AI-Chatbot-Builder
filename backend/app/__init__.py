# backend/app/initial_data.py
import logging
import asyncio

# --- Import the ASYNC engine from session.py ---
from app.db.session import async_engine

# --- Import Base FROM app.db.base (after models are registered there) ---
from app.db.base import Base

# ... (rest of the logging and async init_db function remains the same,
#      using Base.metadata and async_engine) ...

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    logger.info("Creating initial database tables (async)...")
    logger.info(f"Base metadata tables BEFORE create: {Base.metadata.tables.keys()}")
    if not Base.metadata.tables:
         logger.warning("No tables found in Base metadata. Check imports in app/db/base.py!")
         await async_engine.dispose() # Dispose engine if exiting early
         return

    try:
        async with async_engine.begin() as conn:
             await conn.run_sync(Base.metadata.create_all)
        logger.info(f"Base metadata tables AFTER create: {Base.metadata.tables.keys()}")
        logger.info("Database tables created successfully (async).")
    except Exception as e:
        logger.error(f"Error creating database tables (async): {e}")
        logger.error(f"Base metadata tables during error: {Base.metadata.tables.keys()}")
        raise
    finally:
         await async_engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())