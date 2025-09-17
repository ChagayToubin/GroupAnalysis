from pymongo import MongoClient

# חיבור ל-MongoDB שלך (שים את ה-URI האמיתי שלך)
client = MongoClient("mongodb+srv://db_test:123456TEST@cluster0.ziuim0x.mongodb.net/")

# בחירת ה-DB
db = client["telegram_data"]

# בחירת קולקשן (למשל fs.files)
collection = db["fs.files"]

# שליפת כל ה-IDs
ids = collection.distinct("_id")

# הדפסה
print("רשימת כל ה-_id:")
for _id in ids:
    print(_id)
