# app/crud/crud_data_source.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from app.db.models.data_source import DataSource
from app.schemas.data_source import DataSourceCreate, ProcessingStatus
from typing import Optional

async def get_data_source(db: AsyncSession, data_source_id: int) -> DataSource | None:
    """Gets a single data source by ID."""
    result = await db.execute(select(DataSource).filter(DataSource.id == data_source_id))
    return result.scalars().first()

async def create_data_source(
    db: AsyncSession, *, data_source_in: DataSourceCreate, chatbot_id: int, filename: Optional[str] = None
) -> DataSource:
    """Creates a new data source record."""
    db_data_source = DataSource(
        chatbot_id=chatbot_id,
        type=data_source_in.type,
        uri=data_source_in.uri,
        # content=data_source_in.content, # If storing content directly
        filename=filename,
        status=ProcessingStatus.PENDING # Explicitly set initial status
    )
    db.add(db_data_source)
    await db.commit()
    await db.refresh(db_data_source)
    return db_data_source

async def update_data_source_status(
    db: AsyncSession, *, data_source_id: int, status: ProcessingStatus
) -> DataSource | None:
    """Updates the status of a data source."""
    # Option 1: Fetch, update attribute, commit (tracks object)
    # db_obj = await get_data_source(db, data_source_id)
    # if not db_obj: return None
    # db_obj.status = status
    # db.add(db_obj)
    # await db.commit()
    # await db.refresh(db_obj)
    # return db_obj

    # Option 2: Direct update statement (more efficient for single field)
    result = await db.execute(
        update(DataSource)
        .where(DataSource.id == data_source_id)
        .values(status=status)
        .returning(DataSource) # Return the updated row
    )
    await db.commit() # Commit after execute for update/delete
    updated_obj = result.scalars().first()
    return updated_obj

# Add functions later to get status, list data sources, etc.
async def get_data_source_status(db: AsyncSession, data_source_id: int) -> ProcessingStatus | None:
    """Gets the status of a data source."""
    result = await db.execute(
        select(DataSource.status).filter(DataSource.id == data_source_id)
    )
    status_enum = result.scalars().first()
    return status_enum