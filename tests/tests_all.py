import json
from Basetest import BaseTest
from app.models.models import QuestionsModels
from app.models.answer_models import AnswersModels
from app.models.user_models import UserModel
from app.views.views import Questions
from app.views.answer_views import get_single_question


class TestAll(BaseTest):
    question = {
        'title': 'What is json?',
        'body': 'i wanna know what json is',
        'tags': 'json',
        'Question_ID': '1'
    }

    answer = {
        'body': 'This is the answer body'
    }

    def test_class_initializer(self):
        """ Test Class model"""
        questionmodel = QuestionsModels('html', 'this is a sample question',
                                        'programming', '1')
        usermodel = UserModel('guest@gmail.com', 'password')
        answermodel = AnswersModels('this is a sample question')
        self.assertIsInstance(questionmodel, QuestionsModels)
        self.assertIsInstance(usermodel, UserModel)
        self.assertIsInstance(answermodel, AnswersModels)

    def test_post_question(self):
        """Test API can post a question"""
        res = self.client.post('/api/v1/questions',
                               content_type='application/json',
                               data=json.dumps(self.question))
        print(res)
        self.assertEqual(res.status_code, 201)

    def test_get_all_questions(self):
        """Test API can view all questions"""
        res = self.client.get('api/v1/questions',
                              content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_get_one_question(self):
        """Tests API can view only one question"""
        res = self.client.get('api/v1/questions/2',
                              content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_post_an_answer(self):
        """Test API can post_an_answer"""
        self.client.post('/api/v1/questions',
                         content_type='application/json',
                         data=json.dumps(self.question))
        self.client.get('api/v1/questions/1',
                        content_type='application/json')
        res = self.client.post('api/v1/questions/1/answers',
                               content_type='application/json',
                               data=json.dumps(self.answer))
        self.assertEqual(res.status_code, 400)

    def test_delete_question(self):
        """ Test whether a question is deleted """
        self.client.post('/api/v1/questions',
                         content_type='application/json',
                         data=json.dumps(self.question))
        res = self.client.delete('/api/v1/questions/1',
                                 content_type='application/json')
        reply = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
