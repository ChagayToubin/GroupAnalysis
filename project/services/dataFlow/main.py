from project.services.dataFlow.mongoDB import DAL

from project.services.dataFlow.group_type_analyzer import DataFlow

class Menger:
    def __init__(self):
        self.data = DAL()
        self.classifier = DataFlow()

    def menger(self,url):
        all_data = self.data.dal(url)
        dic=self.classifier.data_classifier(all_data)
        return dic

