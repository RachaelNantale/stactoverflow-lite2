
from flask import Flask, make_response, jsonify, Blueprint, abort
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required
from app.models.models import QuestionsModels
from DBHandler import MyDatabase
bp = Blueprint('app', __name__)
api = Api(bp)

db = MyDatabase()


class QuestionsList(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No Title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, required=True,
                                   help='Please post a question',
                                   location='json')
        self.reqparse.add_argument('tags', type=str, required=True,
                                   help='Please provide a tag',
                                   location='json')
        super(QuestionsList, self).__init__()

    @jwt_required
    def post(self):
        args = self.reqparse.parse_args()
        question = QuestionsModels(args['title'], args['description'],
                                   args['tags'])

        try:
            created_question = question.create_question()
            print(created_question)
            return created_question
        except Exception:
            return make_response(jsonify({'Message': 'An error occurred please try again'}), 400)

    @jwt_required
    def get(self):
        questions = db.fetch_all_questions()
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
        self.reqparse.add_argument('description', type=str, required=True,
                                   help='Please post a question',
                                   location='json')
        self.reqparse.add_argument('tags', type=str, required=True,
                                   help='Please provide a tag',
                                   location='json')
        super(Question, self).__init__()

    @jwt_required
    def get(self, Question_ID):
        question = db.fetch_single_question(Question_ID)
        if question is not None:
            return make_response(jsonify(question), 200)
        return make_response(jsonify(
            {'message': 'Sorry no questions asked yet'}
        ))

    @jwt_required
    def delete(self, Question_ID):
        """Method for Deleting a Question"""
        delete_qtn = db.delete_record(Question_ID)
        if delete_qtn is not None:
           return {'message': 'Successfully deleted'}
        return {'message': 'Question Id incorrect or doesnot exist'}


api.add_resource(QuestionsList, '/api/v1/questions')
api.add_resource(Question, '/api/v1/questions/<string:Question_ID>')
