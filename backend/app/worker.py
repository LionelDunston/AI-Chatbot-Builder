# app/worker.py  <-- Make sure this is the file you are editing
import os
from celery import Celery
# --- Adjust settings import if needed ---
# If config.py is in app/core/config.py
from app.core.config import settings
# If config.py is directly in app/config.py
# from app.config import settings

# Determine Broker/Backend URLs - prefer environment variables set in compose
broker_url = os.getenv("CELERY_BROKER_URL", settings.CELERY_BROKER_URL if hasattr(settings, 'CELERY_BROKER_URL') else 'redis://redis:6379/0')
result_backend = os.getenv("CELERY_RESULT_BACKEND", settings.CELERY_RESULT_BACKEND if hasattr(settings, 'CELERY_RESULT_BACKEND') else 'redis://redis:6379/0')

# Initialize Celery
# The first argument is the conventional name of the main module where tasks might be auto-discovered
# or where the app is rooted. Using 'app' matches our project structure.
celery_app = Celery(
    "app", # Main application/project name
    broker=broker_url,
    backend=result_backend,
    # List of modules where Celery should look for tasks.
    # Ensure this matches the actual path to your task files.
    include=["app.tasks.process_data"]
)

# Optional Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # result_expires=3600, # Example: Keep results for 1 hour
)

# Optional: Configure Task Routing (Advanced)
# celery_app.conf.task_routes = {'app.tasks.process_data.*': {'queue': 'processing'}}

if __name__ == "__main__":
    # Allows running celery directly using 'python -m app.worker' if needed
    celery_app.start()