# app/api/endpoints/data_sources.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
import os # For path operations
import shutil # For saving file temporarily
import logging

# --- MODIFIED IMPORT SECTION ---
# No longer need: from app import schemas
from app import crud # Keep top-level crud import
# Import specific schemas needed directly from their source files
from app.schemas.data_source import DataSourceCreate, FileUploadResponse, ProcessingStatus, DataSourceType
# Import User schema if needed for type hints or responses (optional here for now)
# from app.schemas.user import UserRead
# -----------------------------
from app.db.models.user import User # Keep DB model imports
from app.db.models.chatbot import Chatbot # Keep DB model imports
from app.api import deps # Keep dependency import
from app.db.session import get_async_db # Keep session import
# --- Import the Celery task ---
from app.tasks.process_data import process_uploaded_file
# ----------------------------

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the router
router = APIRouter()

# --- Define a temporary upload directory ---
# In production, use a persistent volume or cloud storage (S3)
UPLOAD_DIR = "/code/temp_uploads" # Needs to exist inside container
os.makedirs(UPLOAD_DIR, exist_ok=True) # Create if doesn't exist

@router.post(
    "/{chatbot_id}/upload-file",
    response_model=FileUploadResponse, # Use direct schema name
    status_code=status.HTTP_202_ACCEPTED
)
async def upload_file_for_chatbot(
    *,
    db: AsyncSession = Depends(get_async_db),
    chatbot_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    file: UploadFile = File(...)
) -> Any:
    """
    Upload a file (.txt, .pdf, .md supported for now) as a data source
    for a specific chatbot owned by the current user.
    Triggers background processing (stubbed for now).
    """
    # 1. Verify Chatbot ownership
    chatbot = await crud.crud_chatbot.get_chatbot(db, chatbot_id=chatbot_id)
    if not chatbot or chatbot.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found or not authorized",
        )

    # 2. Basic File Validation
    if not file.filename:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided")

    allowed_content_types = ["text/plain", "application/pdf", "text/markdown"]
    if file.content_type not in allowed_content_types:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Supported: {', '.join(allowed_content_types)}"
         )

    # 3. Save file temporarily
    safe_filename = os.path.basename(file.filename)
    temp_file_path = os.path.join(UPLOAD_DIR, f"{chatbot_id}_{current_user.id}_{safe_filename}")
    try:
        with open(temp_file_path, "wb") as buffer:
             shutil.copyfileobj(file.file, buffer)
    except Exception as e:
         logger.error(f"Failed to save uploaded file: {e}", exc_info=True)
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not save file")
    finally:
         await file.close()
    logger.info(f"Temporarily saved file to: {temp_file_path}")

    # 4. Create DataSource DB Record
    # Use imported DataSourceCreate and DataSourceType directly
    data_source_in = DataSourceCreate(
        type=DataSourceType.FILE, # Use imported Enum
        uri=temp_file_path
    )
    try:
        # Ensure crud_data_source exists and is imported via 'app.crud' or directly
        db_data_source = await crud.crud_data_source.create_data_source(
            db=db,
            data_source_in=data_source_in,
            chatbot_id=chatbot_id,
            filename=safe_filename
        )
        logger.info(f"Created DataSource DB record ID: {db_data_source.id} for file: {safe_filename}")
    except Exception as e:
         logger.error(f"Failed to create DataSource record: {e}", exc_info=True)
         os.remove(temp_file_path)
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create data source record")

    # 5. Trigger Background Task
    try:
         task_result = process_uploaded_file.delay(db_data_source.id, temp_file_path)
         logger.info(f"Sent task {task_result.id} to Celery for data_source_id: {db_data_source.id}")
    except Exception as e:
        logger.error(f"Failed to send task to Celery: {e}", exc_info=True)
        # Ensure ProcessingStatus is imported if using it here
        await crud.crud_data_source.update_data_source_status(db=db, data_source_id=db_data_source.id, status=ProcessingStatus.FAILED)
        os.remove(temp_file_path)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to queue processing task")

    # 6. Return Response using imported schema
    return FileUploadResponse( # Use direct schema name
        filename=safe_filename,
        content_type=file.content_type or "unknown",
        message="File accepted for processing."
    )


# --- Optional Status Endpoint ---
@router.get(
    "/data-sources/{data_source_id}/status",
    response_model=ProcessingStatus # Use direct schema name
)
async def get_data_source_processing_status(
    *,
    db: AsyncSession = Depends(get_async_db),
    data_source_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get the processing status of a specific data source."""
    # Ensure crud_data_source is available via 'app.crud' or direct import
    db_data_source = await crud.crud_data_source.get_data_source(db, data_source_id)
    if not db_data_source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data source not found")

    # Ensure crud_chatbot is available via 'app.crud' or direct import
    chatbot = await crud.crud_chatbot.get_chatbot(db, chatbot_id=db_data_source.chatbot_id)
    if not chatbot or chatbot.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data source not found")

    return db_data_source.status