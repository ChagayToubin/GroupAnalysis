from pymongo import MongoClient
from gridfs import GridFSBucket
from bson import ObjectId
import os, shutil


class MongoDBHandler:


    def __init__(self, client : MongoClient, db_name : str, col_name : str) -> None:
        self.client = client
        self.db_name = db_name
        self.col_name = col_name
        self.fs = GridFSBucket(client[db_name], col_name)



    def write_file_from_gridfs(self, file_id, dir_path, file_type = 'bin'):
        file_path = os.path.join(dir_path, f"{file_id}.{file_type}")
        with self.fs.open_download_stream(ObjectId(file_id)) as stream, open(file_path, "wb") as f:
            text = stream.metadata.get("caption", None)
            his_type = stream.metadata.get("category", None)
            shutil.copyfileobj(stream, f)
        return his_type, file_path, text



    def update_metadata_by_id(self, file_id, field, value):
        files_coll = self.client[self.db_name][f"{self.col_name}.files"]
        file_id = ObjectId(file_id)
        files_coll.update_one(
            {"_id": file_id},
            {"$set": {f"metadata.{field}": value}}
        )
