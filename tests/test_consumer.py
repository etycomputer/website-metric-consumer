import unittest
from tests import app_factory


class MyTest(unittest.TestCase):
    app = None

    def setUp(self):
        self.assertTrue(self.app is None)
        self.app = app_factory.build_production_app()
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.app is not None)

    def tearDown(self):
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.app is not None)

    def test_instance_type(self):
        self.assertTrue(isinstance(self.app, app_factory.Consumer))


if __name__ == '__main__':
    unittest.main()
