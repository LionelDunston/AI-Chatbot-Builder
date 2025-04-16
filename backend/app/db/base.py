# File: backend/app/db/base.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings # Import settings to get DATABASE_URL

from app.db.models.base_class import Base

# 2. Import all your actual model classes HERE.
#    This step registers them with Base.metadata BEFORE Base might be used elsewhere.
from app.db.models.user import User
from app.db.models.chatbot import Chatbot
from app.db.models.data_source import DataSource


# Create an asynchronous SQLAlchemy engine instance using the URL from settings
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, # Checks connection health before use
    echo=False # Set to True to see generated SQL statements (useful for debugging)
)

# Create a factory for creating asynchronous database sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,               # Bind the factory to our engine
    class_=AsyncSession,       # Use the async session class
    expire_on_commit=False,    # Keep objects accessible after commit
    autocommit=False,          # Don't automatically commit
    autoflush=False,           # Don't automatically flush
)

# Create a base class for our SQLAlchemy models to inherit from
# All our database table models will inherit from this class
class Base(DeclarativeBase):
    pass

# --- IMPORTANT: Model Imports for Alembic ---
# Although models are defined in separate files, they need to be imported
# somewhere so that Base knows about them when Alembic runs 'autogenerate'.
# Importing them here ensures they are registered with Base.metadata.
from app.db.models.user import User
from app.db.models.chatbot import Chatbot
# Add imports for any new models you create here

# --- Database Session Dependency for FastAPI ---
# This function will be used as a dependency in API endpoints
# to provide a database session for that specific request.
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session # Provide the session to the endpoint
            # If the endpoint finishes without errors, the 'async with'
            # block might handle commit implicitly depending on context,
            # but explicit commit is safer if needed within the endpoint logic.
            # For simplicity now, we assume commit is handled where needed or by endpoint logic.
            # await session.commit() # Can be added here if a general commit-after-request is desired
        except Exception:
            await session.rollback() # Rollback changes if any exception occurred
            raise # Re-raise the exception so FastAPI can handle it
        finally:
            # The 'async with' block automatically handles closing the session,
            # even if errors occur.
            # await session.close() # Not strictly necessary with 'async with'
            pass