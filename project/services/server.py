from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
import threading
import asyncio

from project.services.pull_data.app.telegram_manager import TelegramManager
pull=TelegramManager()

from project.services.dataFlow.main import Menger
data_flow=Menger()



print("server up")

back_app = FastAPI()

back_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# async def gg():
#     for i in range(30):
#         print("@")
#         if i % 1000 == 0:       # כל אלף הדפסות "משחררים" לולאה
#             await asyncio.sleep(0)

class Identifier(BaseModel):
    id: str


@back_app.post("/init")
async def snapshot(data: Identifier):

    # מפעיל שני threads במקביל
    asyncio.create_task(
        pull.monitor_group("https://t.me/here_hebron_news")  )

    # asyncio.create_task(gg())
    # asyncio.create_task(asyncio.to_thread(kafka_blocking))





    print("-----------------8743843874387-----")

    # מחזיר תשובה מיידית ללקוח
    return {"message": f"שתי המשימות עבור {data.id} התחילו לרוץ במקביל"}


@back_app.post("/get_info")
def  get_info(data: Identifier):

    v=data_flow.menger()
    return v
