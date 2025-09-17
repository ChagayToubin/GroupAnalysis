from project.services.classify_server.configs.configs import Configs


with Configs.get_db_con() as db_client:
    with Configs.get_consumer_con() as consumer_con:
        db_handler = Configs.get_db_handler(db_client)
        consumer = Configs.get_consumer(consumer_con)
        text_classified = Configs.get_text_classifier()
        visual_classified = Configs.get_visual_classifier()
        manager = Configs.get_manager(db_handler, consumer, text_classified, visual_classified)
        manager.manage()








