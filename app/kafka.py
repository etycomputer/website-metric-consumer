import logging
from json import loads, dumps
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from config import kafka_producer_config_params, kafka_consumer_config_params, kafka_topic

# https://kafka-python.readthedocs.io/en/master/usage.html
# https://kafka-python.readthedocs.io/_/downloads/en/1.3.3/pdf/


class MyKafkaProducer:
    log = None
    testing = None
    prefix = ''
    producer = None

    def __init__(self, log: logging, test_mode=None):
        self.log = log
        self.testing = test_mode
        self.prefix = '' if self.testing is None else 'testing-'
        self.producer = KafkaProducer(**kafka_producer_config_params)

    def send_measurements(self, measurements=None) -> bool:
        isSuccessful = True
        if measurements is None:
            measurements = []
        try:
            for sample in measurements:
                message = dumps(sample)
                self.producer.send(self.prefix+kafka_topic, message.encode("utf-8"))
        except KafkaError:
            # Decide what to do if produce request failed...
            self.log.error('Failed to send messages to kafka.')
            isSuccessful = False
        finally:
            # closing database connection.
            if self.producer:
                self.producer.flush()

        return isSuccessful


class MyKafkaConsumer:
    log = None
    testing = None
    prefix = ''
    consumer = None

    def __init__(self, log: logging, test_mode=None):
        self.log = log
        self.testing = test_mode
        self.prefix = '' if self.testing is None else 'testing-'
        self.consumer = KafkaConsumer(self.prefix+kafka_topic, **kafka_consumer_config_params)

    def receive_messages(self) -> (bool, list):
        isSuccessful = True
        measurements = []
        try:
            # Call poll twice. First call will just assign partitions for our
            # consumer without actually returning anything

            for i in range(2):
                raw_msgs = self.consumer.poll(timeout_ms=1000)
                for tp, msgs in raw_msgs.items():
                    for msg in msgs:
                        """
                        msg attributes -> { topic, partition, offset, timestamp, timestamp_type, key, value, 
                        headers, checksum, serialized_key_size, serialized_value_size, serialized_header_size}
                        """
                        measurements.append(loads(str(msg.value.decode('utf-8'))))

            # Commit offsets so we won't get the same messages again
            self.consumer.commit()
        except KafkaError:
            # Decide what to do if produce request failed...
            self.log.error('Failed to receiving messages to kafka.')
            isSuccessful = False
        finally:
            # closing database connection.
            if self.consumer:
                self.consumer.commit()

        return isSuccessful, measurements


def create_kafka_producer(test_mode=None) -> MyKafkaProducer:
    return MyKafkaProducer(logging, test_mode)


def create_kafka_consumer(test_mode=None) -> MyKafkaConsumer:
    return MyKafkaConsumer(logging, test_mode)
