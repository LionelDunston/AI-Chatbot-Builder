# app/schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Shared properties
class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str # Receive plain password on creation

# Properties to return via API (doesn't include password)
class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    # Pydantic V2 config for ORM mode
    model_config = ConfigDict(from_attributes=True)

# Properties stored in DB (hashed password) - We might not need a separate schema for this often
# class UserInDB(UserBase):
#     id: int
#     hashed_password: str
#     is_active: bool
#     is_superuser: bool