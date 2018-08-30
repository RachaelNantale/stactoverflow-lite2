import json
from Basetest import BaseTest
from app.models.models import QuestionsModels
from app.models.answer_models import AnswersModels
from app.models.user_models import UserModel


class TestValidation(BaseTest):
    question = {
        'title': 'What is jsony?',
        'description': 'i wanna know what json is',
        'tags': 'json'
    }

    answer = {
        'description': 'This is the answer description'
    }

    def test_check_duplicate_data(self):
        """Test for Duplicate data"""
        payload = self.user_login()
        self.client.post('/api/v1/questions',
                         content_type='application/json',
                         headers=dict(
                             Authorization='Bearer ' + payload),
                         data=json.dumps(self.question))
        res = self.client.post('/api/v1/questions',
                               content_type='application/json',
                               headers=dict(
                                   Authorization='Bearer ' + payload),
                               data=json.dumps(self.question))
        self.assertEqual(res.status_code, 400)
        self.assertIn('Question already exists', str(res.data))

    def test_if_symbols_are_input(self):
        """ Test whether the client has input data"""
        res = self.client.post('/api/v1/auth/signup',
                               content_type='application/json',
                               data={
                                   'email': '@!#$$',
                                   'password': '123abc'})
        reply = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertTrue("'Please  donot use symbols'", reply['message'])

    def test_if_fields_left_blank(self):
        payload = self.user_login()
        """ Test whether the client has input data"""
        res = self.client.post('/api/v1/questions',
                               content_type='application/json',
                               headers=dict(
                                   Authorization='Bearer ' + payload),
                               data={'title': "  ",
                                     'description': 'rachael@sample.com',
                                     'tags': '123abc'})
        reply = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertTrue(
            "Title is too short. Please add more clarity", reply['message'])

    def test_for_wrong_url(self):
        """Test whether the right url has been input"""
        payload = self.user_login()
        res = self.client.post('/api/v1/questions/',
                               content_type='application/json',
                               headers=dict(
                                   Authorization='Bearer ' + payload),
                               data=json.dumps(self.question))
        self.assertEqual(res.status_code, 404)
        #self.assertIn('404 Not Found ', str(res.data))
