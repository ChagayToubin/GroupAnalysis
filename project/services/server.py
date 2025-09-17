from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import asyncio

from project.services.pull_data.app.telegram_manager import TelegramManager

pull = TelegramManager()

from project.services.dataFlow.main import Menger

data_flow = Menger()

print("server up")

back_app = FastAPI()

back_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Identifier(BaseModel):
    id: str


@back_app.post("/init")
async def init(data: Identifier):
    print(type(data))

    asyncio.create_task(
        pull.monitor_group(data.id))

    return {"message": f"שתי המשימות עבור {data.id} התחילו לרוץ במקביל"}


@back_app.post("/get_info")
def get_info(data: Identifier):
    v = data_flow.menger(data.id)

    return v
