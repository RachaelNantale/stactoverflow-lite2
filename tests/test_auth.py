import json
from Basetest import BaseTest
from app.models.models import QuestionsModels
from app.models.answer_models import AnswersModels
from app.models.user_models import UserModel


class TestAll(BaseTest):

    signup = {
        'User_ID': '1',
        'email': 'guest@email.com',
        'password': 'password'
    }

    login = {
        'email': 'guest@email.com',
        'password': 'password'
    }

    def test_user_signup(self):
        """ Test API can signup user"""
        res = self.client.post('/api/v1/auth/signup',
                               content_type='application/json',
                               data=json.dumps(self.signup))

        self.assertEqual(res.status_code, 201)
        self.assertIn('Created succesfully', str(res.data))

    def test_user_login(self):
        """Test API can login user """
        self.client.post('/api/v1/auth/signup',
                         content_type='application/json',
                         data=json.dumps(self.signup))
        res = self.client.post('/api/v1/auth/login',
                               content_type='application/json',
                               data=json.dumps(self.login))

        self.assertTrue(res.status_code, 200)
        self.assertIn('user successful logged in', str(res.data))

    def test_acces_endpoint_without_token(self):
        ''' Tests API can access protected routes'''
        res = self.client.post('/api/v1/questions',
                               data=json.dumps({'Question_ID': '1wq',
                                                'title': 'What is jsony?',
                                                'description': 'i wanna know what json is',
                                                'tags': 'json',
                                                'asked_by': 'joan'}),
                               content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertIn('Missing Authorization Header', str(res.data))
