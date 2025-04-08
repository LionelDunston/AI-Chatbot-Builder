# app/schemas/token.py
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Schema for the access token response."""
    access_token: str
    token_type: str # Typically "bearer"

class TokenData(BaseModel):
    """Schema for the data encoded within the JWT token."""
    # 'sub' (subject) is a standard JWT claim, often used for user ID/email
    sub: Optional[str] = None