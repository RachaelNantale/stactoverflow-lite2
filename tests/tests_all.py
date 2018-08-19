import json
from Basetest import BaseTest
from app.models.models import QuestionsModels
from app.models.answer_models import AnswersModels
from app.views.views import QUESTIONS
from app.views.answer_views import get_single_question


class TestAll(BaseTest):
    question = {
        'title': 'What is json?',
        'body': 'i wanna know what json is',
        'tags': 'json',
        'qtn_id': '1'
    }

    answer = {
        'body': 'This is the answer body'
    }

    def test_class_initializer(self):
        """ Test Class model"""
        questionmodel = QuestionsModels('html', 'this is a sample question',
                                        'programming', '1')
        self.assertIsInstance(questionmodel, QuestionsModels)

    def test_post_question(self):
        """Test API can post a question"""
        res = self.client.post('/api/v1/questions',
                               content_type='application/json',
                               data=json.dumps(self.question))
        print(res)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Question Created', str(res.data))

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
        

    def test_answer_class_initializer(self):
        """ Test  Answer Class model"""
        answermodel = AnswersModels('this is a sample question')
        self.assertIsInstance(answermodel, AnswersModels)

    def test_get_single_question(self):
        """Test Method for Single Question"""
        single_qtn = get_single_question(self.question['qtn_id'])
        print(single_qtn)
        self.assertTrue(single_qtn['title'], 'What is json?')

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
        self.assertEqual(res.status_code, 201)
        self.assertIn('Answer Created', str(res.data))
