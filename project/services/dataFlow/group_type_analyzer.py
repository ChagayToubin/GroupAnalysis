

class DataFlow:
    def __init__(self):
        pass
    @staticmethod
    def data_classifier(my_dict):
        my_json = {}
        my_count = 0
        json_to_send = {}

        for k,v in my_dict.items():
            if k not in my_json:
                my_json[k] = 0
            if v == "text":
                my_json[k] += my_dict[v] * 8
                my_count += my_dict[v] * 8

            elif v == "video":
                my_json[k] += my_dict[v] * 7
                my_count += my_dict[v] * 7

            elif v == "audio":
                my_json[k] += my_dict[v] * 6
                my_count += my_dict[v] * 6

            elif v == "audio":
                my_json[k] += my_dict[v] * 6
                my_count += my_dict[v] * 6

        for k ,v in my_json.items():
            if v == 0 or my_count == 0:
                json_to_send[k] = 0
            else:
                json_to_send[k] = round(v * 100 / my_count ,1)
        return json_to_send
