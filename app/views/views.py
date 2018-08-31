
from flask import Flask, make_response, jsonify, Blueprint, abort
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import QuestionsModels
from DBHandler import MyDatabase
bp = Blueprint('app', __name__)
api = Api(bp)

db = MyDatabase()


class QuestionsList(Resource):
    """Represents the Question API end point. It has the methods of 
    POST, GET . it takes in parameters from the `QuestionsModels"""

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
        """Method creates a question"""
        args = self.reqparse.parse_args()
        logged_in_user = get_jwt_identity()
        current_user = logged_in_user

        question = QuestionsModels(args['title'], args['description'],
                                   args['tags'], current_user)

        try:
            created_question = question.create_question()
            return created_question
        except Exception:
            return make_response(jsonify({'Message': 'An error occurred please try again'}), 400)

    def get(self):
        """Gets all questions"""
        questions = db.fetch_all_questions()
        if len(questions) == 0:
            return {'message': 'Sorry no questions asked yet'}, 400

        return jsonify({'message': questions})


class Question(Resource):
    """Represents the Questions API end point which need an Id to be 
    passed in order to be triggered. It has the methods of GET, DELETE.
    it takes in parameters from the `QuestionsModels` class """
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
        """Get a questin by Id"""
        question = db.fetch_single_question(Question_ID)
        if question is not None:
            return make_response(jsonify(question), 200)
        return make_response(jsonify(
            {'message': 'Sorry no questions asked yet'}
        ))

    @jwt_required
    def delete(self, Question_ID):
       
        """Method for Deleting a Question"""
        try:
            delete_qtn = db.delete_record(Question_ID)
            return delete_qtn
        except:
            return{'message': 'Question ID doesnot exist'}


api.add_resource(QuestionsList, '/api/v1/questions')
api.add_resource(Question, '/api/v1/questions/<string:Question_ID>')
