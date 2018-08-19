from flask import Flask, make_response, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from app.models.answer_models import AnswersModels
from app.views.views import QUESTIONS
answer_bp = Blueprint('answer_app', __name__)
api = Api(answer_bp)


def get_single_question(qtn_id):
    """ this helper function gets a single question """
    for question in QUESTIONS:
        if question.qtn_id == qtn_id:
            return question


class Answers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('body', type=str, required=True,
                                   help='Please fill in an answer',
                                   location='json')
        super(Answers, self).__init__()

    def post(self, qtn_id):
        args = self.reqparse.parse_args()
        my_answer = AnswersModels(args['body'])
        question = get_single_question(qtn_id)
        question.answers.append(my_answer.to_answerjson())

        return make_response(jsonify({
            'Question': question.__dict__,
            'message': 'Answer Created Created',
            'status': 'success'
        }), 201)


api.add_resource(Answers, '/api/v1/questions/<int:qtn_id>/answers')
