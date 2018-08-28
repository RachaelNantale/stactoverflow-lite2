
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

        # if isinstance(question, QuestionsModels):
        #     for Question in Questions:
        #         if Question.title == args['title']:
        #             return make_response(jsonify({'message':
        #                                           'Question already exists'}
        #                                          ), 400)
        try:
            question.create_question()
            response = {
                'Title': question.title,
                'Description': question.description,
                'Tags': question.tags
            }
            return make_response(jsonify(response), 201)
        except Exception:
            return question

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
        if len(question) == 0:
            return make_response(jsonify(
                {'message': 'Sorry no questions asked yet'}
            ))
        return make_response(jsonify(question), 200)

    @jwt_required
    def delete(self, Question_ID):
        """Method for Deleting a Question"""
        delete_qtn = db.delete_record(Question_ID)
        if len(delete_qtn) == 0:
            abort(404)
        return {'message': 'Successfully deleted'}


api.add_resource(QuestionsList, '/api/v1/questions')
api.add_resource(Question, '/api/v1/questions/<string:Question_ID>')
