import json
from Basetest import BaseTest
from app.models.models import QuestionsModels
from app.models.answer_models import AnswersModels
# from app.views.views import Questions
from app.views.answer_views import get_single_question
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
        self.client.post('/api/v1/questions',
                         content_type='application/json',
                         data=json.dumps(self.question))

        res = self.client.post('/api/v1/questions',
                               content_type='application/json',
                               data=json.dumps(self.question))

        self.assertEqual(res.status_code, 400)
        self.assertIn('Question already exists', str(res.data))
