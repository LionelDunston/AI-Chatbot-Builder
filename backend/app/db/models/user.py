# backend/app/db/models/user.py

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING # Import TYPE_CHECKING

# Correctly import Base using relative path within the 'models' package
from .base_class import Base

# Use TYPE_CHECKING block for imports needed only for type hinting
# to prevent runtime circular dependency issues with Chatbot.
if TYPE_CHECKING:
    from .chatbot import Chatbot # Correct relative import for Chatbot type hint

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False)

    # SQLAlchemy's relationship uses string reference "Chatbot".
    # The TYPE_CHECKING import above is only needed if you explicitly use
    # the 'Chatbot' type elsewhere in this file for type hinting purposes.
    chatbots: Mapped[List["Chatbot"]] = relationship(
        "Chatbot",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"