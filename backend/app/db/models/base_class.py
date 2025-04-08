# app/db/models/base_class.py  <-- Note the path
from sqlalchemy.orm import DeclarativeBase
from typing import Any

class Base(DeclarativeBase):
    id: Any
    pass