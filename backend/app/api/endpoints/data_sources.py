# backend/app/api/endpoints/data_sources.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional
import os
import shutil
import logging

# --- Adjusted Schema Imports ---
from app.schemas.data_source import FileUploadResponse, DataSourceCreate, DataSourceType, ProcessingStatus
# -----------------------------
# --- Adjusted CRUD Imports ---
# Assuming you have __init__.py in crud making submodules accessible
# Or import directly: from app.crud import crud_chatbot, crud_data_source
from app import crud
# -------------------------
from app.db.models.user import User
from app.db.models.chatbot import Chatbot # Keep for type hint clarity if needed
from app.api import deps
from app.db.session import get_async_db
# --- Import the Celery task ---
from app.tasks.process_data import process_uploaded_file
# ----------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# --- Define temporary upload directory (NEEDS proper configuration/volume for workers) ---
# This path MUST be accessible with the same path by both the API container and the Worker container
# A named volume mounted to the same path in both services in docker-compose.yml is recommended.
UPLOAD_DIR = "/code/temp_uploads" # Example path inside container
os.makedirs(UPLOAD_DIR, exist_ok=True) # Ensure directory exists

@router.post(
    "/{chatbot_id}/upload-file",
    response_model=FileUploadResponse,
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
    Upload a file (.txt, .pdf, .md currently suggested) as a data source
    for a specific chatbot owned by the current user.

    Saves the file temporarily, creates a database record, and triggers
    background processing via Celery.
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

    # Sanitize filename (basic example)
    safe_filename = os.path.basename(file.filename)
    # Create a more unique temporary filename if needed (e.g., using uuid)
    temp_file_path = os.path.join(UPLOAD_DIR, f"{chatbot_id}_{current_user.id}_{safe_filename}")

    # 3. Save File Temporarily
    try:
        logger.info(f"Attempting to save uploaded file to: {temp_file_path}")
        with open(temp_file_path, "wb") as buffer:
             shutil.copyfileobj(file.file, buffer)
        logger.info(f"Successfully saved file to: {temp_file_path}")
    except Exception as e:
         logger.error(f"Failed to save uploaded file '{safe_filename}': {e}", exc_info=True)
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not save file")
    finally:
         # Ensure the UploadFile resource is closed
         await file.close()

    # 4. Create DataSource DB Record
    db_data_source: Optional[DataSource] = None # Define variable scope
    data_source_in = DataSourceCreate(
        type=DataSourceType.FILE,
        uri=temp_file_path # Store the path where the file was saved
    )
    try:
        # Make sure crud.crud_data_source exists and has create_data_source
        db_data_source = await crud.crud_data_source.create_data_source(
            db=db,
            data_source_in=data_source_in,
            chatbot_id=chatbot_id,
            filename=safe_filename # Store the original (sanitized) filename
        )
        logger.info(f"Created DataSource DB record ID: {db_data_source.id} for file: {safe_filename}")
    except Exception as e:
        logger.error(f"Failed to create DataSource record for file '{safe_filename}': {e}", exc_info=True)
        # Cleanup the saved file if DB record creation fails
        try:
            os.remove(temp_file_path)
            logger.info(f"Cleaned up temporary file: {temp_file_path}")
        except OSError as remove_err:
            logger.error(f"Error cleaning up file {temp_file_path} after DB error: {remove_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create data source record")

    # 5. Trigger Background Processing Task
    try:
        # Ensure db_data_source is not None before accessing id
        if db_data_source:
            task_result = process_uploaded_file.delay(db_data_source.id, temp_file_path)
            logger.info(f"Sent task {task_result.id} to Celery for data_source_id: {db_data_source.id}")
        else:
             # This case should ideally not happen if DB creation succeeded, but handle defensively
             raise ValueError("db_data_source is None after successful creation attempt.")

    except Exception as e:
        logger.error(f"Failed to send task to Celery for file '{safe_filename}': {e}", exc_info=True)
        # Attempt to mark DB record as FAILED and clean up file
        if db_data_source:
            try:
                await crud.crud_data_source.update_data_source_status(
                    db=db, data_source_id=db_data_source.id, status=ProcessingStatus.FAILED
                )
                logger.info(f"Marked DataSource {db_data_source.id} as FAILED due to Celery queueing error.")
            except Exception as update_err:
                 logger.error(f"Failed to mark DataSource {db_data_source.id} as FAILED: {update_err}")
        try:
            os.remove(temp_file_path)
            logger.info(f"Cleaned up temporary file: {temp_file_path} after Celery error")
        except OSError as remove_err:
            logger.error(f"Error cleaning up file {temp_file_path} after Celery error: {remove_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to queue processing task")

    # 6. Return Success Response
    return FileUploadResponse(
        filename=safe_filename,
        content_type=file.content_type or "unknown",
        message="File accepted for processing."
        # data_source_id=db_data_source.id # Optionally return the ID
    )


# --- Optional: Endpoint to get data source status ---
@router.get(
    "/data-sources/{data_source_id}/status",
    response_model=ProcessingStatus # Return just the status enum
)
async def get_data_source_processing_status(
    *,
    db: AsyncSession = Depends(get_async_db),
    data_source_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get the processing status of a specific data source."""
    # Ensure crud.crud_data_source exists and has get_data_source
    db_data_source = await crud.crud_data_source.get_data_source(db, data_source_id)
    if not db_data_source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data source not found")

    # Verify chatbot ownership by fetching the associated chatbot
    chatbot = await crud.crud_chatbot.get_chatbot(db, chatbot_id=db_data_source.chatbot_id)
    if not chatbot or chatbot.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data source not found") # Mask ownership

    return db_data_source.status # Return the status enum directly

# Add other data source related endpoints here later (e.g., list data sources for a chatbot)