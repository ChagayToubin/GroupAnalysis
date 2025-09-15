

class DataFlow:
    def __init__(self):
        self.my_json = {}
        self.my_count = 0
        self.json_to_send = {}
        self.my_db = ""


    def data_classifier(self,my_dict:dict):
        if my_dict["name"] != self.my_db:
            self.my_db = my_dict["name"]
            self.my_json = {}
            self.my_count = 0
            self.json_to_send = {}
        k,v = next(iter(my_dict.items()))
        if k == "text":
            if v in self.my_json:
                self.my_json[v] += 8
                self.my_count += 8
            else:
                self.my_json[v] = 8
                self.my_count += 8

        elif k == "video":
            if v in self.my_json:
                self.my_json[v] += 7
                self.my_count += 7
            else:
                self.my_json[v] = 7
                self.my_count += 7

        elif k == "audio":
            if v in self.my_json:
                self.my_json[v] += 6
                self.my_count += 6
            else:
                self.my_json[v] = 6
                self.my_count += 6

        elif k == "image":
            if v in self.my_json:
                self.my_json[v] += 5
                self.my_count += 5
            else:
                self.my_json[v] = 5
                self.my_count += 5
        else:
            return "not found this type!"

        for i ,b in self.my_json.items():
            self.json_to_send[i] = round(b * 100 / self.my_count ,1)

        return [self.json_to_send,self.my_db]


alist = [
  {"text": "terror","name":"dasa"},
  {"video": "violence"},
  {"audio": "music"},
  {"image": "nature"},
  {"text": "news"},
  {"video": "terror"},
  {"text": "music"},
  {"audio": "violence"},
  {"image": "news"},
  {"text": "nature"},
  {"video": "music"},
  {"audio": "terror"},
  {"image": "violence"},
  {"text": "news"},
  {"video": "nature"},
  {"audio": "music"},
  {"text": "terror"},
  {"image": "news"},
  {"video": "violence"},
  {"text": "nature"},
  {"audio": "terror"},
  {"video": "music"},
  {"image": "nature"},
  {"text": "violence"},
  {"audio": "news"},
  {"video": "terror"},
  {"text": "music"},
  {"image": "news"},
  {"audio": "violence"},
  {"text": "terror"},
  {"tex": "terror"}
]



a = DataFlow()
for i in alist:
    print(a.data_classifier(i))


