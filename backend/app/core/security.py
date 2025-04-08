from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone # Import datetime components
from typing import Any, Union # For type hinting
from jose import jwt # Import jwt from python-jose
from app.core.config import settings # Import settings

# Use bcrypt for hashing passwords
# schemes=["bcrypt"] ensures only bcrypt is used
# deprecated="auto" handles potential future changes in default schemes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY # Get from settings
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES # Get from settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password using bcrypt."""
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Creates a JWT access token.

    :param subject: The subject of the token (e.g., user email or ID).
    :param expires_delta: Optional timedelta for expiration. If None, uses default from settings.
    :return: The encoded JWT token string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    # Data to encode in the token payload
    to_encode = {"exp": expire, "sub": str(subject)}
    # Encode the token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt