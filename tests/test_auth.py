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
