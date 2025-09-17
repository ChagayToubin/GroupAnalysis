class DataFlow:
    def __init__(self):
        pass

    @staticmethod
    def data_classifier(my_dict):
        my_json = {}
        my_count = 0
        json_to_send = {}

        for category, types in my_dict.items():
            if category not in my_json:
                my_json[category] = 0

            for t, count in types.items():
                if t == "text":
                    my_json[category] += count * 8
                    my_count += count * 8
                elif t == "video":
                    my_json[category] += count * 7
                    my_count += count * 7
                elif t == "audio":
                    my_json[category] += count * 6
                    my_count += count * 6
                elif t == "image":
                    my_json[category] += count * 5
                    my_count += count * 5

        for k, v in my_json.items():
            if v == 0 or my_count == 0:
                json_to_send[k] = 0
            else:
                json_to_send[k] = round(v * 100 / my_count, 1)

        return json_to_send
