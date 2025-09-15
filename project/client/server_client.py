from fastapi import FastAPI

client_root = FastAPI(title="Client App")

@client_root.get("/")
async def home_client():
    return {"msg": "Hello from Client"}
