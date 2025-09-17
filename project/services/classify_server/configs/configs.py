import os
import json
import torch
import open_clip
import torch.nn.functional as F
from project.services.classify_server.objects.mongodb_connection import MongoDBConnection
from project.services.classify_server.fetcher.mongodb_handler.mongodb_handler import MongoDBHandler
from project.services.classify_server.objects.kafka_consumer_connection import KafkaConsumerConnection
from project.services.classify_server.fetcher.mongodb_handler.my_kafka_consumer import MyKafkaConsumer
from project.services.classify_server.ai_class.text_classified import TextClassified
from project.services.classify_server.ai_class.visual_classified import VisualClassified
from project.services.classify_server.maneger.maneger import Manager


class Configs:

    categories_classification = os.getenv("CATEGORIES", "Terrorism,financial,sexual,leisure").split(",")

    kafka_host = os.getenv("KAFKA_HOST", "localhost")
    kafka_port = os.getenv("KAFKA_PORT", "9092")
    topic = os.getenv("KAFKA_TOPIC", 'telegram_messages')
    group_id = os.getenv("GROUP_ID", "my-consumer")

    kafka_configs = {
        'bootstrap_servers': [f"{kafka_host}:{kafka_port}"],
        'group_id': group_id,
        'auto_offset_reset': "earliest",
        'enable_auto_commit': 'True',
        'value_deserializer': lambda v: json.loads(v.decode("utf-8"))
    }

    mongodb_uri = os.getenv("MONGODB_URI", "mongodb+srv://db_test:123456TEST@cluster0.ziuim0x.mongodb.net/")

    db_name = os.getenv("DB_NAME", "telegram_data")
    col_name = os.getenv("COL_NAME", "fs")

    openclip_model_name = os.getenv("OPENCLIP_MODEL_NAME", "ViT-B-32")
    openclip_pretrained = os.getenv("OPENCLIP_PRETRAINED", "openai")


    @classmethod
    def init_openclip(cls):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        model, _, preprocess = open_clip.create_model_and_transforms(
            cls.openclip_model_name, pretrained=cls.openclip_pretrained
        )
        model = model.to(device).eval()
        tokenizer = open_clip.get_tokenizer(cls.openclip_model_name)

        def encode_categories(categories):
            tokens = tokenizer(categories).to(device)
            with torch.no_grad():
                vec = model.encode_text(tokens)
            return F.normalize(vec, dim=-1)  # [num_categories, dim]

        encode_cat = encode_categories(cls.categories_classification)

        return {
            "model": model,
            "preprocess": preprocess,
            "tokenizer": tokenizer,
            "device": device,
            "encode_categories": encode_cat,
        }

    @classmethod
    def get_db_con(cls):
        return MongoDBConnection(cls.mongodb_uri)

    @classmethod
    def get_db_handler(cls, client):
        return MongoDBHandler(client, cls.db_name, cls.col_name)

    @classmethod
    def get_consumer_con(cls):
        return KafkaConsumerConnection([cls.topic] ,cls.kafka_configs)

    @classmethod
    def get_consumer(cls, client):
        return MyKafkaConsumer(client)


    @classmethod
    def get_visual_classifier(cls):
        visual_configs = cls.init_openclip()
        return VisualClassified(**visual_configs)


    @classmethod
    def get_text_classifier(cls):
        return TextClassified(cls.categories_classification)

    @classmethod
    def get_manager(cls, db_handler, consumer, text_classified, visual_classified):
        return Manager(db_handler, consumer, text_classified, visual_classified, cls.categories_classification)






