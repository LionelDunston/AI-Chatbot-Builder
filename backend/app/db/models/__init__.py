# app/db/models/__init__.py
from .base_class import Base # Expose Base if needed
from .user import User       # Explicitly import and expose User
from .chatbot import Chatbot # Explicitly import and expose Chatbot
# Import other models here if you want them accessible via app.db.models.ModelName