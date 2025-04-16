# app/db/models/data_source.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
import enum # Keep enum import here if needed
from typing import Optional
from .base_class import Base
# Import schemas to use Enums defined there
from app.schemas.data_source import DataSourceType, ProcessingStatus

class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chatbot_id: Mapped[int] = mapped_column(Integer, ForeignKey("chatbots.id"), nullable=False)
    type: Mapped[DataSourceType] = mapped_column(SQLEnum(DataSourceType, name="datasourcetype"), nullable=False)
    status: Mapped[ProcessingStatus] = mapped_column(SQLEnum(ProcessingStatus, name="processingstatus"), default=ProcessingStatus.PENDING, nullable=False)
    uri: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True) # File path, URL, etc.
    # Consider a larger text field if storing full text content directly (less common for large docs)
    # content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Store original filename for file uploads
    filename: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationship back to Chatbot (optional but good practice)
    # chatbot: Mapped["Chatbot"] = relationship(back_populates="data_sources")
    # Note: Need to add 'data_sources: Mapped[List["DataSource"]] = relationship(back_populates="chatbot")' to Chatbot model if using back_populates

    def __repr__(self):
        return f"<DataSource(id={self.id}, type='{self.type.name}', chatbot_id={self.chatbot_id})>"