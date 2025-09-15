from mongoDB import DAL

from group_type_analyzer import DataFlow

data = DAL()
classifier = DataFlow()
skip = 0
def main():

    all_data = data.dal(skip)


    for doc in all_data:
        classifier.data_classifier(doc)

if __name__ == "__main__":
    while True:
        main()