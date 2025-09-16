from GroupAnalysis.classify_server.configs.configs import (Configs ,
                                                           MongoDBConnection ,
                                                           MongoDBHandler ,
                                                           KafkaConsumerConnection,
                                                           MyKafkaConsumer,
                                                           TextClassified,
                                                           VisualClassified,
                                                           Manager)


with MongoDBConnection(Configs.mongodb_uri) as mdbc:
    with KafkaConsumerConnection([Configs.topic],Configs.get_kafka_configs()) as kcc:
        mdbh = MongoDBHandler(mdbc, Configs.db_name, Configs.col_name)
        kc = MyKafkaConsumer(kcc)
        tc = TextClassified(Configs.categories)
        vc = VisualClassified(**Configs.init_openclip())
        m = Manager(mdbh, kc, tc, vc, Configs.categories)
        m.manage()








