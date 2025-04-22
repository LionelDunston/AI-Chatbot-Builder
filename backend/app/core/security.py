# backend/app/core/security.py

from datetime import datetime, timedelta, timezone # Ensure timezone is imported
from typing import Any, Union # For type hinting

from jose import jwt, JWTError # Import jwt and potential error class
from passlib.context import CryptContext

from app.core.config import settings # Import your application settings

# 1. Password Hashing Setup
# --------------------------
# Use bcrypt for hashing passwords.
# schemes=["bcrypt"] ensures only bcrypt is used.
# deprecated="auto" handles potential future changes in default schemes.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against its hashed version.

    :param plain_password: The password provided by the user.
    :param hashed_password: The hash stored in the database.
    :return: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password using the configured context (bcrypt).

    :param password: The plain text password to hash.
    :return: The generated password hash string.
    """
    return pwd_context.hash(password)


# 2. JWT Token Creation Setup
# ---------------------------
# Retrieve JWT settings from the central configuration
ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY # Ensure this is loaded correctly in config.py
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Creates a JWT access token containing subject information and an expiration date.

    :param subject: The subject of the token (typically user ID). Should be convertible to string.
    :param expires_delta: Optional timedelta object for custom expiration.
                          If None, default expiration from settings is used.
    :return: The encoded JWT access token as a string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Data to encode in the token payload
    # 'exp': Expiration time claim (required by many JWT validators)
    # 'sub': Subject claim (conventionally holds the user identifier)
    to_encode = {"exp": expire, "sub": str(subject)} # Ensure subject is stringified for JWT standard

    # Encode the payload into a JWT string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Encoding with SECRET_KEY starting with: {SECRET_KEY[:5]}...") # Temporary debug print

    return encoded_jwt

# Note: You might later add functions here for decoding/verifying tokens
# if needed outside the FastAPI dependency context, but for now,
# the dependency in deps.py handles verification.