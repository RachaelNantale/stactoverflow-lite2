import unittest
import json
from app import create_app
from instance.config import TestingConfig
from DBHandler import MyDatabase


class BaseTest (unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        db = MyDatabase()
        db.create_tables()

    def user_login(self):
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json',
                         data=json.dumps({'User_ID': '1',
                                          'email': 'rachael@guest.com',
                                          'password': 'password'}))
        res = self.client.post('/api/v1/auth/login',
                               content_type='application/json',
                               data=json.dumps({'email': 'rachael@guest.com',
                                                'password': 'password'}))

        payload = json.loads(res.data.decode())
        return payload['token']

    def tearDown(self):
        db = MyDatabase()
        db.drop_tables()
        db.create_tables()


if __name__ == "__main__":
    unittest.main()
