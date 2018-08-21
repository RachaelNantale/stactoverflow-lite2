
from flask import Flask, make_response, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from app.models.models import QuestionsModels
bp = Blueprint('app', __name__)
api = Api(bp)

QUESTIONS = []


class QuestionsList(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No Title provided',
                                   location='json')
        self.reqparse.add_argument('body', type=str, required=True,
                                   help='Please post a question',
                                   location='json')
        self.reqparse.add_argument('tags', type=str, required=True,
                                   help='Please provide a tag',
                                   location='json')
        super(QuestionsList, self).__init__()

    def post(self):
        qtn_id = len(QUESTIONS)
        qtn_id += 1
        args = self.reqparse.parse_args()
        question = QuestionsModels(args['title'], args['body'],
                                   args['tags'], qtn_id)
        QUESTIONS.append(question)
        return make_response(jsonify({
            'question': question.__dict__,
            'message': 'Question Created',
            'status': 'success'
        }), 201)

    def get(self):
        question_rides = [question.__dict__ for question in QUESTIONS]
        return make_response(jsonify(question_rides), 200)


class Question(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No Title provided',
                                   location='json')
        self.reqparse.add_argument('body', type=str, required=True,
                                   help='Please post a question',
                                   location='json')
        self.reqparse.add_argument('tags', type=str, required=True,
                                   help='Please provide a tag',
                                   location='json')
        super(Question, self).__init__()

    def get(self, qtn_id):
        question = [
            question.__dict__ for question in QUESTIONS if question.qtn_id == qtn_id]
        return make_response(jsonify(question), 200)


api.add_resource(QuestionsList, '/api/v1/questions')
api.add_resource(Question, '/api/v1/questions/<int:qtn_id>')
