import logging
from app import database, kafka
from time import sleep
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


class Consumer:
    log = None
    pg_db = None
    kafka_c = None

    def __init__(self, pg_db: database.MyPostgresDB, kafka_c: kafka.MyKafkaConsumer, log: logging):
        self.log = log
        self.pg_db = pg_db
        self.kafka_c = kafka_c

    def run(self):
        try:
            while True:
                isSuccessful, measurements = self.kafka_c.receive_messages()
                if isSuccessful:
                    self.log.info("Received {} messages from Kafka".format(len(measurements)))
                    self.pg_db.insert_measurements(measurements)
                else:
                    self.log.error("Error while receiving message from kafka.")
                sleep(5)
        except KeyboardInterrupt:
            self.log.info("Exiting the background task.")


def create_consumer() -> Consumer:
    pg_db = database.create_postgres_db()
    kafka_c = kafka.create_kafka_consumer()
    return Consumer(pg_db, kafka_c, logging)
