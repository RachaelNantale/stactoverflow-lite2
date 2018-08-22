
from flask import Flask, make_response, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from app.models.models import QuestionsModels
bp = Blueprint('app', __name__)
api = Api(bp)

Questions = []


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
        Question_ID = len(Questions)
        Question_ID += 1
        args = self.reqparse.parse_args()
        question = QuestionsModels(args['title'], args['body'],
                                   args['tags'], Question_ID)
        Questions.append(question)
        return make_response(jsonify({
            'question': question.__dict__,
        }), 201)

    def get(self):
        questions = [question.__dict__ for question in Questions]
        if len(questions) == 0:
            return make_response(jsonify(
                {'message': 'Sorry no questions asked yet'}
            ))
        return make_response(jsonify(questions), 200)


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

    def get(self, Question_ID):
        question = [
            question.__dict__ for question in Questions if question.Question_ID == Question_ID]
        if len(question) == 0:
            return make_response(jsonify(
                {'message': 'Sorry no questions asked yet'}
            ))
        return make_response(jsonify(question), 200)


api.add_resource(QuestionsList, '/api/v1/questions')
api.add_resource(Question, '/api/v1/questions/<int:Question_ID>')
