import unittest
from tests import app_factory
from config import integration_mode
from datetime import datetime, timezone


class MyKafkaConsumerTest(unittest.TestCase):
    my_kafka_p = None
    my_kafka_c = None

    def setUp(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        self.assertTrue(self.my_kafka_p is None)
        self.my_kafka_p = app_factory.build_kafka_producer(True)
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.my_kafka_p is not None)
        self.assertTrue(self.my_kafka_c is None)
        self.my_kafka_c = app_factory.build_kafka_consumer(True)
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.my_kafka_c is not None)

    def tearDown(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.my_kafka_p is not None)
        self.assertTrue(self.my_kafka_c is not None)

    def test_instance_type(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        self.assertTrue(isinstance(self.my_kafka_p, app_factory.MyKafkaProducer))
        self.assertTrue(isinstance(self.my_kafka_c, app_factory.MyKafkaConsumer))

    def test_ping_pong(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        messages = [[1, datetime.now(timezone.utc).__str__(), 200, 23.23, True]]
        self.my_kafka_p.send_measurements(messages)
        isSuccessful, measurement_results = self.my_kafka_c.receive_messages()
        self.assertTrue(isSuccessful)
        self.assertEqual(messages, measurement_results)


if __name__ == '__main__':
    unittest.main()
