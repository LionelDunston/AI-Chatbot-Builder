# File: backend/app/core/config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache 
# Load .env file if it exists (for local overrides without compose)
# Useful if you want to run locally without docker-compose sometimes
load_dotenv()

class Settings(BaseSettings):
    # This class loads settings from environment variables.
    # Pydantic automatically matches environment variables (case-insensitive)
    # to the attributes defined here.

    # Database Configuration - Reads from DATABASE_URL env var set in docker-compose.yml
    DATABASE_URL: str

    # JWT Settings (for authentication later)
    # Reads from SECRET_KEY env var set in docker-compose.yml
    SECRET_KEY: str = '5ec013a38996783fa42aca842f498411f0cc9e6dd9e0050b1f1297e1f7219e5e'
    ALGORITHM: str = "HS256" # Algorithm for JWT signing
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # How long access tokens are valid

    class Config:
        # If you were using a .env file heavily, you'd specify it here
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # Pydantic v2 uses model_config instead of Config class for some settings
        # but env_file is still supported here for now.


# Use lru_cache to create a singleton Settings instance
# This prevents reading .env file or env vars multiple times
@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Create an instance of the Settings class.
# This instance will be imported and used throughout the application.
settings = Settings()

# You could add print statements here for debugging during startup if needed
# print(f"Loaded DATABASE_URL: {settings.DATABASE_URL}")
# print(f"Loaded SECRET_KEY: {'*' * 6}{settings.SECRET_KEY[-4:]}") # Avoid printing full key