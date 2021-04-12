from app import consumer, database
from app.consumer import Consumer
from app.database import MyPostgresDB


def build_production_app() -> Consumer:
    app = consumer.create_consumer()
    return app


def build_postgres_db(test_mode=True) -> MyPostgresDB:
    db = database.create_producer(test_mode)
    return db
