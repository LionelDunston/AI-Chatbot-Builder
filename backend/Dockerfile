# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir reduces image size
# --upgrade pip ensures we have the latest pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# This includes main.py and any other .py files you add later
COPY . .

# Command to run the application when the container starts
# Uses uvicorn to run the FastAPI app (main:app)
# --host 0.0.0.0 makes it accessible from outside the container
# --port 80 is the standard HTTP port we'll map to
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
# File: backend/Dockerfile (last line)

# OLD: CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
# NEW: Point to app.main:app and add --reload for development volume mount
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]