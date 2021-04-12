import unittest
from tests import app_factory
from config import integration_mode


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


if __name__ == '__main__':
    unittest.main()
