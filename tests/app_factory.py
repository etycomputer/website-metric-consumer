from app import consumer
from app.consumer import Consumer


def build_production_app() -> Consumer:
    app = consumer.create_consumer()
    return app
