import unittest
import re
from tests import app_factory


class MyPostgresTest(unittest.TestCase):
    my_db = None

    def setUp(self):
        self.assertTrue(self.my_db is None)
        self.my_db = app_factory.build_postgres_db(True)
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.my_db is not None)

    def tearDown(self):
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.my_db is not None)

    def test_instance_type(self):
        self.assertTrue(isinstance(self.my_db, app_factory.MyPostgresDB))

    def test_drop_db(self):
        result = self.my_db.drop_db()
        self.assertEqual(2, len(result))
        for query_cmd in result:
            re.compile(r"^testing_$", re.IGNORECASE).match(query_cmd)

    def test_create_db(self):
        result = self.my_db.create_db()
        self.assertEqual(3, len(result))
        for query_cmd in result:
            re.compile(r"^testing_$", re.IGNORECASE).match(query_cmd)

    def test_seed_db(self):
        result = self.my_db.seed_db()
        self.assertEqual(1, len(result))
        for query_cmd in result:
            re.compile(r"^testing_$", re.IGNORECASE).match(query_cmd)


if __name__ == '__main__':
    unittest.main()
