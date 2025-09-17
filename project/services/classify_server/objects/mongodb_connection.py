from pymongo import MongoClient

class MongoDBConnection:

    def __init__(self, uri):
        self.uri = uri
        self.client = None


    def __enter__(self):
        self.open()
        return self.client


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type is not None:
            print(f"An exception occurred: {exc_val}")
        return False


    def open(self):
        try:
            self.client = MongoClient(self.uri)
        except Exception as e:
            raise RuntimeError("Failed to connect to MongoDB") from e


    def close(self):
        if self.client:
            self.client.close()
            self.client = None