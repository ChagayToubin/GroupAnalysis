from project.services.dataFlow.mongoDB import DAL

from project.services.dataFlow.group_type_analyzer import DataFlow
from datetime import datetime


class Menger:
    def __init__(self):
        self.data = DAL()
        self.classifier = DataFlow()

    def menger(self,url):
        all_data = self.data.dal(url)
        dic=self.classifier.data_classifier(all_data)
        keys = list(dic.keys())

        dic_all = {
            "id": url,
            "updatedAt": datetime.utcnow().isoformat() + "Z",
            "results": {
                "metrics": [
                    {"name": keys[0], "value": dic[keys[0]]},
                    {"name": keys[1], "value": dic[keys[1]]},
                    {"name": keys[2], "value": dic[keys[2]]},
                    {"name": keys[3], "value": dic[keys[3]]}
                ]
            },
            "version": 3
        }
        print(dic_all)
        return dic_all

