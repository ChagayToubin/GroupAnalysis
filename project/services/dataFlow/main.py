from project.services.dataFlow.mongoDB import DAL

from project.services.dataFlow.group_type_analyzer import DataFlow

class Menger:
    def __init__(self):
        self.data = DAL()
        self.classifier = DataFlow()

    def menger(self):
        all_data = self.data.dal("https://t.me/+ztOtIXepdDVkYjE0")
        dic=self.classifier.data_classifier(all_data)
        return dic
#
#
# if __name__ == "__main__":
#     start = Menger()
#     while True:
#         print("ds")
#         start.menger()