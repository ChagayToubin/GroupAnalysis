import os


class Settings:
    # ---------------- MongoDB ----------------
    MONGO_URI= os.getenv(
        "MONGO_URI",
        "mongodb+srv://db_test:123456TEST@cluster0.ziuim0x.mongodb.net/"
    )

    # ---------------- ElasticSearch ----------------
    ELASTIC_URI= os.getenv("ELASTIC_URI", "http://localhost:9200")

    # ---------------- Kafka ----------------
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "default_topic")
