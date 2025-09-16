from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Create app instance
back_app = FastAPI()

# 👇 הוספת CORS מיד אחרי יצירת ה־app
back_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # אפשר לשים ["http://localhost:3000"] אם אתה רוצה לאפשר רק לפרונט שלך
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Identifier(BaseModel):
    id: str

@back_app.post("/api/snapshot")
async def home(data: Identifier):
    print(data)

    return {"message": "לחגדלגדחלדגחלגדחלחגדמנלחגדמלחנגדלחנגדלחגדנלחגדנלחגדנ"}
