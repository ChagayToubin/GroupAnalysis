from mongoDB import DAL

from group_type_analyzer import DataFlow

class Menger:
    def __init__(self):
        self.data = DAL()
        self.classifier = DataFlow()

    def menger(self):
        all_data = self.data.dal("https://t.me/+ztOtIXepdDVkYjE0")
        self.classifier.data_classifier(all_data)

if __name__ == "__main__":
    start = Menger()
    while True:
        start.menger()