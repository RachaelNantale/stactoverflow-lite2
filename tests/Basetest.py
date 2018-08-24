import unittest
from app import create_app
from instance.config import TestingConfig
from app.views.views import Questions
import json


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.Test_Questions = []

    def check_duplicate_data(self):
        """Test for Duplicate data"""
        self.client.post('/api/v1/questions',
                         content_type='application/json',
                         data=json.dumps({
                             'title': 'What is jsony?',
                             'description': 'i wanna know what json is',
                             'tags': 'json'
                         }))

        res = self.client.post('/api/v1/questions',
                               content_type='application/json',
                               data=json.dumps({
                                   'title': 'What is jsony?',
                                   'description': 'i wanna know what json is',
                                   'tags': 'json'
                               }))
        data = json.loads(res.data.decode())

    def tearDown(self):
        self.Test_Questions = []


if __name__ == "__main__":
    unittest.main(verbosity=2)
