import pymongo


class DAL:
    def __init__(self):
        myclient = pymongo.MongoClient("mongodb+srv://db_test:123456TEST@cluster0.ziuim0x.mongodb.net/")
        mydb = myclient["telegram_data"]
        self.mycol = mydb["fs.files"]
        self.classify_categories = ["neutral","teror","safe","suspicious"]
        self.types = ["text","video","audio","image"]

    def dal(self,group_name):
        my_dict = {}
        for category in self.classify_categories:
            my_dict[category] = {}
            for type in self.types:
                my_dict[category][type] = self.mycol.count_documents({"metadata.group_link":group_name,"metadata.category":type,"metadata.classify":category})

        return my_dict