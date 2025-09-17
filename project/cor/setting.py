import os
import json

class Settings:
    # ---------------- MongoDB ----------------
    MONGO_URI= os.getenv(
        "MONGO_URI",
        "mongodb+srv://db_test:123456TEST@cluster0.ziuim0x.mongodb.net/"
    )

    # ---------------- ElasticSearch ----------------
    ELASTIC_URI= os.getenv("ELASTIC_URI", "http://localhost:9200")

    # ---------------- Kafka ----------------
    kafka_host = os.getenv("KAFKA_HOST", "localhost")
    kafka_port = os.getenv("KAFKA_PORT", 9092)

    configs_for_kafka_pro = {
        'bootstrap_servers': f"{kafka_host}:{kafka_port}",
        'value_serializer': lambda v: json.dumps(v).encode('utf-8')

    }
    configs_for_kafka_con = {
        'bootstrap_servers': f"{kafka_host}:{kafka_port}",
        'group_id': "my-consumer",
        'auto_offset_reset': "earliest",
        'enable_auto_commit': 'True',
        'value_deserializer': lambda v: json.loads(v.decode("utf-8"))
    }
