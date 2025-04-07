# File: backend/alembic/env.py (near the top)
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine # <--- ADD

# --- ADD THESE IMPORTS ---
import os
import sys
import asyncio
from app.core.config import settings # Import your app settings
from app.db.base import Base # Import your Base model

from app.db.base import Base # <--- Import your Base
               # <--- Import os
              # <--- Import sys

# --- Add imports for your model modules HERE ---
from app.db.models import user # Import the user module
from app.db.models import chatbot # Import the chatbot module

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


      

# File: backend/alembic/env.py (replace the existing run_migrations_online function)

def do_run_migrations(connection):
    """Helper function to run migrations within a synchronous context."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """Create an async engine and run migrations within an async connection."""
    # Create async engine using the DATABASE_URL from settings
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool # Use NullPool for migrations
    )

    async with connectable.connect() as connection:
        # Run the actual migrations within the connection's run_sync method
        await connection.run_sync(do_run_migrations)

    # Dispose of the engine explicitly
    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode by running the async migration function."""
    # Use asyncio.run to execute the async migration function
    asyncio.run(run_async_migrations())


# --- This part should already exist at the bottom of the file ---
# --- Make sure it calls the correct function ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online() # Ensure this calls the function defined above