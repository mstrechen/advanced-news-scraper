from time import sleep

from elasticsearch_dsl import connections
from flask import Flask
from admin.models.articles_es import ArticleTextEs


MODELS = [ArticleTextEs, ]


def init_es(app: Flask):
    conn = connections.create_connection(hosts=app.config['ELASTICSEARCH_HOSTS'], timeout=20)
    for _ in range(10 * 60 // 5):  # timeout of 60 seconds
        if conn.ping():
            break
        app.logger.error("Failed to ping elasticsearch, retrying in 5 second...")
        sleep(5)
    if app.config['MODE'] == 'MIGRATE':
        for es_model in MODELS:
            es_model.init()
