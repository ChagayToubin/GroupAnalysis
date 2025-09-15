from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
# Create app instance
back_app = FastAPI()


class StringDict(BaseModel):
    data: Dict[str, str]


# Simple route
@back_app.post("/start")
async def home(data:StringDict):
    print(data)
    # פו מתחיל כל התהליך ברגע שהוא מקבל להתחיל לפעול והוא מקבל את הבקשה

    return {"message": data}


