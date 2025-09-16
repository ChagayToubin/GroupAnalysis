import pymongo


class DAL:
    def __init__(self):
        myclient = pymongo.MongoClient("mongodb+srv://db_test:123456TEST@cluster0.ziuim0x.mongodb.net/")
        mydb = myclient["telegram_data"]
        self.mycol = mydb["fs.files"]

    def dal(self,skiper):
        my_list = []
        a = self.mycol.find({},{"metadata.category":1,"metadata.group_link":1,"metadata.classify":1,"_id":0}).skip(skiper)
        for i in a:
            my_list.append(i["metadata"])
        return my_list

