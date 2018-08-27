from flask import Flask, make_response, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required
from app.models.answer_models import AnswersModels
from app.models.models import QuestionsModels
from app.views.views import Questions
from app.utilities.utilities import validate_answer_input
answer_bp = Blueprint('answer_app', __name__)
api = Api(answer_bp)


def get_single_question(Question_ID):
    """ this helper function gets a single question """
    for question in Questions:
        if question.Question_ID == Question_ID:
            return question


class Answers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, required=True,
                                   help='Please fill in an answer',
                                   location='json')
        super(Answers, self).__init__()

    @jwt_required
    def post(self, Question_ID):
        args = self.reqparse.parse_args()
        my_answer = validate_answer_input(args['answer'])
        question = get_single_question(Question_ID)
        if isinstance(my_answer, AnswersModels):
            if not isinstance(question, QuestionsModels):
                return make_response(jsonify({
                    'message': 'Please choose a question before you answer'
                }), 400)
            question.answers.append(my_answer.to_answerjson())
            return make_response(jsonify({
                'Question': question.__dict__
            }), 201)
        return my_answer


api.add_resource(Answers, '/api/v1/questions/<string:Question_ID>/answers')
