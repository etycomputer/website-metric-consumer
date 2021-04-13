import unittest
from tests import app_factory
from config import integration_mode
from datetime import datetime, timezone


class MyPostgresTest(unittest.TestCase):
    my_db = None

    def setUp(self):
        self.assertTrue(self.my_db is None)
        self.my_db = app_factory.build_postgres_db(False)
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.my_db is not None)

    def tearDown(self):
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.my_db is not None)

    def test_instance_type(self):
        self.assertTrue(isinstance(self.my_db, app_factory.MyPostgresDB))

    def test_drop_create_seed_drop_db(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        self.assertTrue(self.my_db.drop_db())
        self.assertTrue(self.my_db.create_db())
        self.assertTrue(self.my_db.seed_db())
        self.assertTrue(self.my_db.drop_db())

    def test_get_urls(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        self.assertTrue(self.my_db.drop_db())
        self.assertTrue(self.my_db.create_db())
        self.assertTrue(self.my_db.seed_db())
        url_result = self.my_db.get_urls()
        self.assertEqual(2, len(url_result))
        for url in url_result:
            self.assertEqual(4, len(url_result[url]))
            self.assertEqual({'url_id', 'sample_frequency_s', 'url_path', 'regex_pattern'}, url_result[url].keys())
        self.assertTrue(self.my_db.drop_db())

    def test_insert_measurements(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        measurements = [
            [6, datetime.now(timezone.utc).__str__(), 200, 1.166535, True],
            [5, datetime.now(timezone.utc).__str__(), 200, 2.170638, True]
        ]
        self.assertTrue(self.my_db.drop_db())
        self.assertTrue(self.my_db.create_db())
        self.assertTrue(self.my_db.seed_db())
        isSuccessful = self.my_db.insert_measurements(measurements)
        self.assertTrue(isSuccessful)
        self.assertTrue(self.my_db.drop_db())


if __name__ == '__main__':
    unittest.main()
