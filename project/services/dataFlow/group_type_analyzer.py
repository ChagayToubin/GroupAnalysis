

class DataFlow:
    def __init__(self):
        self.my_json = {}
        self.my_count = 0
        self.json_to_send = {}
        self.my_db = ""


    def data_classifier(self,my_dict):
        if my_dict["group_link"] != self.my_db:
            self.my_db = my_dict["group_link"]
            self.my_json = {}
            self.my_count = 0
            self.json_to_send = {}

        else:
            if my_dict["category"] == "text":
                if my_dict["classify"] in self.my_json:
                    self.my_json[my_dict["classify"]] += 8
                    self.my_count += 8
                else:
                    self.my_json[my_dict["classify"]] = 8
                    self.my_count += 8

            elif my_dict["category"] == "video":
                if my_dict["classify"] in self.my_json:
                    self.my_json[my_dict["classify"]] += 7
                    self.my_count += 7
                else:
                    self.my_json[my_dict["classify"]] = 7
                    self.my_count += 7

            elif my_dict["category"] == "audio":
                if my_dict["classify"] in self.my_json:
                    self.my_json[my_dict["classify"]] += 6
                    self.my_count += 6
                else:
                    self.my_json[my_dict["classify"]] = 6
                    self.my_count += 6

            elif my_dict["category"] == "image":
                if my_dict["classify"] in self.my_json:
                    self.my_json[my_dict["classify"]] += 5
                    self.my_count += 5
                else:
                    self.my_json[my_dict["classify"]] = 5
                    self.my_count += 5
            else:
                return "not found this type!"
            print(self.json_to_send)
            for k ,v in self.my_json.items():
                self.json_to_send[k] = round(v * 100 / self.my_count ,1)
            print(self.json_to_send)
            return self.json_to_send

data = [
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'video', 'classify': 'neutral'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'image', 'classify': 'teror'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'audio', 'classify': 'safe'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'text', 'classify': 'suspicious'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'image', 'classify': 'neutral'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'video', 'classify': 'teror'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'audio', 'classify': 'suspicious'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'text', 'classify': 'safe'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'video', 'classify': 'neutral'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'image', 'classify': 'teror'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'audio', 'classify': 'safe'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'text', 'classify': 'suspicious'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'video', 'classify': 'teror'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'image', 'classify': 'neutral'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'audio', 'classify': 'safe'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'text', 'classify': 'suspicious'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'video', 'classify': 'teror'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'image', 'classify': 'safe'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'audio', 'classify': 'neutral'},
{'group_link': 'https://t.me/BackYardOfficial', 'category': 'text', 'classify': 'suspicious'}
]

a = DataFlow()
for i in data:

    a.data_classifier(i)

