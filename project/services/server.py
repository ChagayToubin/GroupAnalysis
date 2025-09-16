from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
import threading
from project.services.dataFlow.main import skip


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

# משימה ראשונה
def task_one(task_id: str):
    print(f"Task 1 started for {task_id}")
    time.sleep(20)  # סימולציה של עבודה ארוכה
    print(f"Task 1 finished for {task_id}")

# משימה שנייה
def task_two(task_id: str):
    print(f"Task 2 started for {task_id}")
    time.sleep(40)  # סימולציה של עבודה יותר ארוכה
    print(f"Task 2 finished for {task_id}")

@back_app.post("/init")
async def snapshot(data: Identifier):
    # מפעיל שני threads במקביל
    t1 = threading.Thread(target=task_one, args=(data.id,))
    # תהליך ראשון מתחיל למשוך דאטה
    t2 = threading.Thread(target=task_two, args=(data.id,))
    # תהליך שני של ניתוח הדברים ועידכונם בתוך הדאטה ביס
    t1.start()
    t2.start()
    # מחזיר תשובה מיידית ללקוח
    return {"message": f"שתי המשימות עבור {data.id} התחילו לרוץ במקביל"}


@back_app.post("/get_info")
async  def  get_info(data: Identifier):
    # תהליך של צבי
    print(data)

    return {"assa":"תהלחך שמחשב כמה יש עכשיו בדאטה ביס מכל דבר"}