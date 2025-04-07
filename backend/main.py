from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a path operation decorator for the root path ("/")
# This tells FastAPI that the function below handles GET requests to "/"
@app.get("/")
async def read_root():
    # Return a simple JSON response
    return {"message": "Hello World"}

# Define another endpoint
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
     # item_id uses Python type hints for automatic validation
     # q is an optional query parameter (e.g., /items/5?q=somequery)
     return {"item_id": item_id, "q": q}