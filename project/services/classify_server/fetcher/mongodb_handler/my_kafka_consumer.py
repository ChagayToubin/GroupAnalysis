from kafka import KafkaConsumer

class MyKafkaConsumer:

    def __init__(self, client : KafkaConsumer):
        self.client = client


    def consume(self):
        for msg in self.client:
            yield msg