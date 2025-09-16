from kafka import KafkaConsumer
from project.utilities.logger.logger_info import Logger

logger=Logger.get_logger()

class MyKafkaConsumer:

    def __init__(self, topics , configs ) :
        self.topics = topics
        self.configs = configs
        self.consumer = None


    def open(self):
        try:
            self.consumer = KafkaConsumer(*self.topics, **self.configs)
        except Exception as e:
            print(type(e).__name__, "-", e)
            raise RuntimeError(f"Kafka connect failed: {type(e).__name__} - {e}") from e


    def close(self):
        if self.consumer:
            self.consumer.close()


    def consume(self):
        for msg in self.consumer:
            yield msg