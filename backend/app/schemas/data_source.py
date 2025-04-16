# app/schemas/data_source.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
import enum
from typing import Optional

# Enum for different source types we'll support later
class DataSourceType(str, enum.Enum):
    FILE = "file"
    WEBSITE = "website"
    TEXT = "text"
    # Add more later: CSV, JSON, DB, API, etc.

# Enum for processing status
class ProcessingStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class DataSourceBase(BaseModel):
    type: DataSourceType
    uri: Optional[str] = None # URL for website, file path/id, etc.
    content: Optional[str] = None # For direct text input

class DataSourceCreate(DataSourceBase):
    # Input for creating a source - might be simpler initially
    pass

class DataSourceRead(DataSourceBase):
    id: int
    chatbot_id: int
    status: ProcessingStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    # Maybe add filename for FILE type

    model_config = ConfigDict(from_attributes=True)

# Response model for file uploads specifically
class FileUploadResponse(BaseModel):
    filename: str
    content_type: str
    message: str
    # data_source_id: Optional[int] = None # Could add later