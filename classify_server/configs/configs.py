import os
import json
import torch
import open_clip
import torch.nn.functional as F
from GroupAnalysis.classify_server.objects.mongodb_connection import MongoDBConnection
from GroupAnalysis.classify_server.fetcher.mongodb_handler.mongodb_handler import MongoDBHandler
from GroupAnalysis.classify_server.objects.kafka_consumer_connection import KafkaConsumerConnection
from GroupAnalysis.classify_server.fetcher.mongodb_handler.my_kafka_consumer import MyKafkaConsumer
from GroupAnalysis.classify_server.ai_class.text_classified import TextClassified
from GroupAnalysis.classify_server.ai_class.visual_classified import VisualClassified
from GroupAnalysis.classify_server.maneger.maneger import Manager


class Configs:

    categories = os.getenv("CATEGORIES", "Terrorism,financial,sexual,leisure").split(",")

    kafka_host = os.getenv("KAFKA_HOST", "localhost")
    kafka_port = os.getenv("KAFKA_PORT", "9092")
    topic = os.getenv("KAFKA_TOPIC", 'topic_name')
    group_id = os.getenv("GROUP_ID", "my-consumer")

    @classmethod
    def get_kafka_configs(cls):
        return {
            'bootstrap_servers': [f"{cls.kafka_host}:{cls.kafka_port}"],
            'group_id': cls.group_id,
            'auto_offset_reset': "earliest",
            'enable_auto_commit': 'True',
            'value_deserializer': lambda v: json.loads(v.decode("utf-8"))
        }


    mongodb_uri = os.getenv("MONGODB_URI", "mongodb+srv://db_test:123456TEST@cluster0.ziuim0x.mongodb.net/")

    db_name = os.getenv("DB_NAME", "telegram_data")
    col_name = os.getenv("COL_NAME", "fs")


    @classmethod
    def init_openclip(cls, model_name: str = "ViT-B-32", pretrained: str = "openai"):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        model, _, preprocess = open_clip.create_model_and_transforms(
            model_name, pretrained=pretrained
        )
        model = model.to(device).eval()
        tokenizer = open_clip.get_tokenizer(model_name)


        def encode_categories(categories):
            tokens = tokenizer(categories).to(device)
            with torch.no_grad():
                vec = model.encode_text(tokens)
            return F.normalize(vec, dim=-1)  # [num_categories, dim]


        return {
            "model": model,
            "preprocess": preprocess,
            "tokenizer": tokenizer,
            "device": device,
            "encode_categories": encode_categories(cls.categories),
        }