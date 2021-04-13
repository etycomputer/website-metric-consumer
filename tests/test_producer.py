import unittest
from tests import app_factory
from config import integration_mode


class MyProducerTest(unittest.TestCase):
    app = None

    def setUp(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        self.assertTrue(self.app is None)
        self.app = app_factory.build_production_app()
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.app is not None)

    def tearDown(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        # Make sure app is passed in correctly and has correct type
        self.assertTrue(self.app is not None)

    def test_instance_type(self):
        if integration_mode is False:
            self.assertTrue(True)
            return
        self.assertTrue(isinstance(self.app, app_factory.Producer))


if __name__ == '__main__':
    unittest.main()
