# backend/app/db/session.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings # Import settings for DATABASE_URL

# --- Engine Creation ---
async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    # echo=True # Uncomment for debugging SQL
)
# ---------------------

# --- Session Maker Creation ---
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
# --------------------------

# --- ASYNC Dependency Function ---
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency generator for async database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback() # Optional: Rollback on exception within endpoint
            raise
        # finally: # Not strictly needed as 'async with' handles close
        #    await session.close()
# -------------------------------

# --- REMOVE get_db() if it was synchronous ---