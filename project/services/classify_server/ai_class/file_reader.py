class FileReader:

    @staticmethod
    def load_file(fetch = "data/yamnet_list.txt"):
        with open(fetch, "r", encoding="utf-8") as f:
            return f.read()