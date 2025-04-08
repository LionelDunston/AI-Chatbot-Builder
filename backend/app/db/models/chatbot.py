# backend/app/db/models/chatbot.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from typing import TYPE_CHECKING # Import TYPE_CHECKING

# Correctly import Base using relative path within the 'models' package
from .base_class import Base

# Correctly import the Enum from the schemas module where it's defined
from app.schemas.chatbot import ChatbotStatus

# Use TYPE_CHECKING block for imports needed only for type hinting
# to prevent runtime circular dependency issues with User.
if TYPE_CHECKING:
    from .user import User # Correct relative import for User type hint

class Chatbot(Base):
    __tablename__ = "chatbots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Use the imported Enum for the column type, adding explicit DB name
    status: Mapped[ChatbotStatus] = mapped_column(
        SQLEnum(ChatbotStatus, name="chatbotstatus", create_type=False), # Use create_type=False if type exists
        default=ChatbotStatus.PENDING,
        nullable=False
    )
    # Note: If using Alembic migrations later, managing Enum types requires care.
    # create_type=False might be needed if the type is managed by Alembic. Start without it if unsure.

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # SQLAlchemy's relationship uses string reference "User".
    # The TYPE_CHECKING import above is only needed if you explicitly use
    # the 'User' type elsewhere in this file for type hinting purposes.
    owner: Mapped["User"] = relationship("User", back_populates="chatbots")

    def __repr__(self):
        return f"<Chatbot(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"