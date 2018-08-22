from flask import Flask, make_response, jsonify, Blueprint, abort
from flask_restful import Resource, Api, reqparse
from app.models.models import QuestionsModels
from flask_jwt_extended import jwt_required
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
        """ Method for Creating a Question"""
        Question_ID = len(Questions)
        Question_ID += 1
        args = self.reqparse.parse_args()
        question = QuestionsModels(args['title'], args['body'],
                                   args['tags'], Question_ID)
        Questions.append(question)

        response = {
            'title': question.title,
            'Description': question.body,
            'Tags': question.tags,
            'Time Created': question.time
        }
        return make_response(jsonify(
            response
        ), 201)

    def get(self):
        """Method for Getting all questions created """
        questions = [question.__dict__ for question in Questions]
        if len(questions) == 0:
            return make_response(jsonify(
                {'message': 'Sorry no questions asked yet'}
            ))
        return make_response(jsonify(questions), 200)


class Question(Resource):
    """ This Class takes in all methods that need an ID"""
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
        """ Method for getting only one question by ID"""
        question = [
            question.__dict__ for question in Questions if question.Question_ID == Question_ID]
        print(question)
        if len(question) == 0:
            return make_response(jsonify(
                {'message': 'Sorry no questions asked yet'}
            ))
        return make_response(jsonify(question), 200)

    def delete(self, Question_ID):
        """Method for Deleting a Question"""
        delete_qtn = [
            qtn for qtn in Questions if qtn.Question_ID == Question_ID]
        if len(delete_qtn) == 0:
            abort(404)
        Questions.remove(delete_qtn[0])
        return {'message': 'Successfully deleted'}


api.add_resource(QuestionsList, '/api/v1/questions')
api.add_resource(Question, '/api/v1/questions/<int:Question_ID>')
