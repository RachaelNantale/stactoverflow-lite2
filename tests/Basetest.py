import unittest
from app import create_app
from instance.config import TestingConfig


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
