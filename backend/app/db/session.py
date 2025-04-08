# app/db/session.py
from typing import AsyncGenerator # <-- Need this for async dependency
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Ensure URL uses the async scheme (optional check, compose should provide it)
async_database_url = settings.DATABASE_URL
if not async_database_url.startswith("postgresql+asyncpg"):
    # Handle error or try to fix, but ideally docker-compose provides correct URL
    raise ValueError(f"Invalid DATABASE_URL scheme for async: {settings.DATABASE_URL}. Expected 'postgresql+asyncpg://'")

# --- Use ASYNC engine ---
async_engine = create_async_engine(
    async_database_url,
    pool_pre_ping=True,
    # echo=True # Uncomment for debugging SQL statements
)
# ----------------------

# --- Use ASYNC session maker ---
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False # Recommended for async sessions
)
# -----------------------------

# --- ASYNC dependency function ---
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency generator for async database sessions."""
    async with AsyncSessionLocal() as session:
        # Optional: You could yield session.begin() here if you want
        # transactions automatically handled per request block.
        # Requires careful thought about transaction boundaries.
        yield session
# -------------------------------

# --- REMOVE synchronous parts ---
# create_engine(...)
# SessionLocal = sessionmaker(...)
# def get_db(): ...
# --- END REMOVAL ---