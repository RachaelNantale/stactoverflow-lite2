from flask import Flask, make_response, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from app.models.answer_models import AnswersModels
from app.models.models import QuestionsModels
from app.views.views import Questions
answer_bp = Blueprint('answer_app', __name__)
api = Api(answer_bp)


def get_single_question(qtn_id):
    """ this helper function gets a single question """
    for question in Questions:
        if question.qtn_id == qtn_id:
            return question


class Answers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, required=True,
                                   help='Please fill in an answer',
                                   location='json')
        super(Answers, self).__init__()

    def post(self, qtn_id):
        args = self.reqparse.parse_args()
        my_answer = AnswersModels(args['answer'])
        question = get_single_question(qtn_id)
        if not isinstance(question, QuestionsModels):
            return make_response(jsonify({
                'message': 'Please choose a question before you answer'
            }), 400)
        question.answers.append(my_answer.to_answerjson())
        return make_response(jsonify({
            'Question': question.__dict__
        }), 201)


api.add_resource(Answers, '/api/v1/questions/<int:qtn_id>/answers')
