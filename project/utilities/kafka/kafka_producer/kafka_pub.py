from kafka import KafkaProducer

class Producer:

    def __init__(self, configs):
        self.configs = configs
        self.producer = None


    def open(self):
        try:
            self.producer = KafkaProducer(**self.configs)
        except Exception as e:
            raise RuntimeError("Failed to connect to Kapka.") from e


    def close(self):
        if self.producer:
            self.producer.close()


    def send_to_kafka(self, topic_name, data):
        try:
            self.producer.send(topic_name, data)

        except Exception as e:
            raise RuntimeError("Failed to send to Kapka") from e