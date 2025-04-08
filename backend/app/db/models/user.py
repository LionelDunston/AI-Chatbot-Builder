# File: backend/app/db/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base # Import the Base class from base.py
from .base_class import Base

class User(Base):
    # Tells SQLAlchemy the name of the table in the database
    __tablename__ = "users"

    # Define columns for the 'users' table
    id = Column(Integer, primary_key=True, index=True) # Auto-incrementing primary key
    email = Column(String, unique=True, index=True, nullable=False) # User's email, must be unique
    hashed_password = Column(String, nullable=False) # Store hashed password, never plain text
    is_active = Column(Boolean(), default=True) # Flag to activate/deactivate user

    # Define the relationship to the Chatbot model
    # 'chatbots' will be a list of Chatbot objects associated with this user
    # 'back_populates' links this relationship to the 'owner' attribute in the Chatbot model
    chatbots = relationship("Chatbot", back_populates="owner", cascade="all, delete-orphan")
