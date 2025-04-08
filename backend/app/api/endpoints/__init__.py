# backend/app/api/endpoints/__init__.py

# Explicitly import the router from each endpoint file
from .users import router as users_router
from .chatbots import router as chatbots_router
from .login import router as login_router