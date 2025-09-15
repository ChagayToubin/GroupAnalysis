from fastapi import FastAPI

# Create app instance
back_app = FastAPI()

# Simple route
@back_app.get("/")
async def home():
    return {"message": "Hello, FastAPI is running!"}

# Another route
@back_app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}, welcome to FastAPI!"}
