# backend/app/schemas/__init__.py

# Import schemas from their respective files to make them
# accessible directly via the 'schemas' package namespace

from .token import Token, TokenPayload # Import Token and TokenPayload from token.py
from .user import UserBase, UserCreate, UserRead # Import user schemas
from .chatbot import ChatbotBase, ChatbotCreate, ChatbotUpdate, ChatbotRead, ChatbotStatus # Import chatbot schemas
from .data_source import ( # Import data source schemas
    DataSourceBase,
    DataSourceCreate,
    DataSourceRead,
    DataSourceType,
    ProcessingStatus,
    FileUploadResponse,
)

# Add any other schema imports here as needed