# File: backend/app/db/models/chatbot.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # For database functions like default timestamps
from app.db.base import Base # Import the Base class
from .base_class import Base # Relative import
from .user import User       

class Chatbot(Base):
    # Tells SQLAlchemy the name of the table in the database
    __tablename__ = "chatbots"

    # Define columns for the 'chatbots' table
    id = Column(Integer, primary_key=True, index=True) # Primary key
    name = Column(String, index=True, nullable=False) # Name of the chatbot
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Timestamp when created (using DB server time)
    # status = Column(String, default="PENDING") # Example: track processing status
    # config = Column(Text) # Example: store JSON config as text

    # Foreign Key linking to the 'users' table (specifically the 'id' column)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Define the relationship back to the User model
    # 'owner' will be the User object associated with this chatbot
    # 'back_populates' links this to the 'chatbots' attribute in the User model
    owner = relationship("User", back_populates="chatbots")