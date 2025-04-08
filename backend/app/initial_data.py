# app/initial_data.py
import logging
import asyncio # Import asyncio

# --- Use the ASYNC engine ---
from app.db.session import async_engine
from app.db.base import Base # Base now knows models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db(): # Make the function async
    logger.info("Creating initial database tables (async)...")
    try:
        # Use run_sync within an async connection context
        async with async_engine.begin() as conn:
             # Pass the synchronous function Base.metadata.create_all
             await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully (async).")
    except Exception as e:
        logger.error(f"Error creating database tables (async): {e}")
        raise
    finally:
         # Gracefully close the engine connections (optional but good practice in scripts)
         await async_engine.dispose()


if __name__ == "__main__":
    # Run the async function using asyncio.run()
    asyncio.run(init_db())