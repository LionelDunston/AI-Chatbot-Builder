# backend/app/db/models/base_class.py
from sqlalchemy.orm import DeclarativeBase
from typing import Any

class Base(DeclarativeBase):
    id: Any
    pass