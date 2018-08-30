import json
from Basetest import BaseTest
from app.models.models import QuestionsModels
from app.models.answer_models import AnswersModels
from app.models.user_models import UserModel


class TestAll(BaseTest):
    question = {
        'Question_ID': '1wq',
        'title': 'What is jsony?',
        'description': 'i wanna know what json is',
        'tags': 'json',
        'asked_by': 'joan'
    }

    answer = {

        'answer': 'This is the answer description',
        'answered_by': 'joan'
    }

    def test_class_initializer(self):
        """ Test Class model"""
        questionmodel = QuestionsModels('html', 'this is a sample question',
                                        'programming', 'joan')
        self.assertIsInstance(questionmodel, QuestionsModels)
        answermodel = AnswersModels('1', 'this is a sample question', 'joan')
        self.assertIsInstance(answermodel, AnswersModels)
        usermodel = UserModel('guest@email.com', 'password')
        self.assertIsInstance(usermodel, UserModel)

    def test_post_question(self):
        """Test API can post a question"""
        payload = self.user_login()
        res = self.client.post('/api/v1/questions',
                               content_type='application/json',
                               headers=dict(
                                   Authorization='Bearer ' + payload),
                               data=json.dumps(self.question))
        self.assertEqual(res.status_code, 201)
        self.assertIn('Created succesfully', str(res.data))

    def test_get_all_questions(self):
        """Test API can view all questions"""
        payload = self.user_login()
        self.client.post('/api/v1/questions',
                         content_type='application/json',
                         headers=dict(
                             Authorization='Bearer ' + payload),
                         data=json.dumps(self.question))

        res = self.client.get('api/v1/questions',
                              content_type='application/json')
        reply = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertIn('What is jsony', str(res.data))

    def test_get_one_question(self):
        """Tests API can view only one question"""
        payload = self.user_login()
        self.client.post('/api/v1/questions',
                         content_type='application/json',
                         headers=dict(
                             Authorization='Bearer ' + payload),
                         data=json.dumps(self.question))

        res = self.client.get('api/v1/questions/1wq',
                              content_type='application/json',
                              headers=dict(
                                  Authorization='Bearer ' + payload),)
        reply = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)

   
    def test_fetch_answers_by_qtnid(self):
        """Test API can fetch an answer by question id"""
        payload = self.user_login()
        self.client.post('/api/v1/questions',
                         content_type='application/json',
                         headers=dict(
                             Authorization='Bearer ' + payload),
                         data=json.dumps(self.question))
        self.client.get('api/v1/questions/1',
                        headers=dict(
                            Authorization='Bearer ' + payload),
                        content_type='application/json'),

        res = self.client.get('api/v1/questions/1/answers',
                              content_type='application/json',
                              headers=dict(
                                  Authorization='Bearer ' + payload),
                              data=json.dumps(self.answer))

        self.assertEqual(res.status_code, 200)
