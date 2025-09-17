from kafka import KafkaConsumer


class KafkaConsumerConnection:

    def __init__(self, topics: list[str], configs: dict) -> None:
        self.topics = topics
        self.configs = configs
        self.consumer = None


    def __enter__(self):
        self.open()
        return self.consumer


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type is not None:
            print(f"An exception occurred: {exc_val}")
        return False


    def open(self):
        try:
            self.consumer = KafkaConsumer(*self.topics, **self.configs)
        except Exception as e:
            print(type(e).__name__, "-", e)
            raise RuntimeError(f"Kafka connect failed: {type(e).__name__} - {e}") from e


    def close(self):
        if self.consumer:
            self.consumer.close()
            self.consumer = None