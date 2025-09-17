

import gridfs
from pymongo import MongoClient
from project.utilities.logger.logger_info import Logger
logger =Logger.get_logger()

class Mongo:
    def __init__(self,mongo_setting):

        self.host = mongo_setting[0]
        self.port = mongo_setting[1]
        self.db_name = mongo_setting[2]
        self.user = mongo_setting[3]
        self.password = mongo_setting[4]

        self.client = None
        self.db = None

    def get_uri(self):
        if self.user and self.password:
            return f"mongodb+srv://{self.user}:{self.password}@{self.host}/{self.db_name}"
        else:
            return f"mongodb://{self.host}:27017/"


    def connect(self):
        try:
            uri = self.get_uri()
            self.client = MongoClient(uri)
            self.db = self.client[self.db_name]
            print(f"connected ")
            logger.info("The connect seccess")
        except Exception as e:
            logger.error(f"the connect faild becuas{e}")


    def close(self):

        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            print("Connection closed")

    def create(self, collection_name, document):

        return self.db[collection_name].insert_one(document)

    def read_all(self, collection_name):

        return list(self.db[collection_name].find())

    def send_audio(self,data_dict,uniq_id):
        fs = gridfs.GridFS(self.db)
        path_folder = r"C:\Users\User\PycharmProjects\MuezzinProject07_09\project\data_files\podcasts"

        audio_file_path = f"{path_folder}/{data_dict["name"]}"
        with open(audio_file_path, "rb") as audio_file:
            file_id = fs.put(audio_file, filename=uniq_id)
            print(file_id)

