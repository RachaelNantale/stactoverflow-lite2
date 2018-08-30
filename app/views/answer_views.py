from flask import Flask, make_response, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.answer_models import AnswersModels
from app.models.models import QuestionsModels
from DBHandler import MyDatabase
answer_bp = Blueprint('answer_app', __name__)
api = Api(answer_bp)

db = MyDatabase()


class AnswerList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, required=True,
                                   help='Please fill in an answer',
                                   location='json')

        super(AnswerList, self).__init__()

    @jwt_required
    def post(self, Question_ID):
        args = self.reqparse.parse_args()
        logged_in_user = get_jwt_identity()
        my_answer = AnswersModels(args['answer'], Question_ID,
                                  logged_in_user)
        try:
            created_answer = my_answer.create_answer()
            return created_answer
        except Exception:
            return {'message': 'An error occured.Please Make sure that the Question exists'}, 404

    @jwt_required
    def get(self, Question_ID):
        try:
            question = db.fetch_all_answers(Question_ID)
            if question is not None:
                return jsonify({'message': question})
        except:
            return make_response(jsonify(
                {'message': 'Sorry the question or answer doesnt exist'}
            ))


class Answers(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('answer', type=str, required=True,
                                   help='Please fill in an answer',
                                   location='json')

    @jwt_required
    def put(self, Question_ID, Answer_ID):
        try:

            args = self.reqparse.parse_args()

            current_user = get_jwt_identity()
            user = db.fetch_user_by_email(email=current_user)
            logged_in_user = user[1]

            answer_exists = db.fetch_answer_by_id(Answer_ID=Answer_ID)
            question_exists = db.fetch_single_question_by_id(
                Question_ID=Question_ID)

            a_owner_email = db.fetch_answer_details(Question_ID, Answer_ID)[4]

            qtn_details = db.fetch_single_question_by_id(
                Question_ID=Question_ID)
            qtn_details_email = qtn_details[4]

            if question_exists:
                if answer_exists:
                    if logged_in_user == a_owner_email:
                        update = db.update_answer(
                            answer=args['answer'], Question_ID=Question_ID,
                            Answer_ID=Answer_ID)
                        updated_answer = db.fetch_answer_details(
                            Question_ID=Question_ID, Answer_ID=Answer_ID)

                    if logged_in_user == qtn_details_email:
                        db.accept_answer(Answer_ID=Answer_ID)
                        updated_answer = db.fetch_answer_details(
                            Question_ID=Question_ID, Answer_ID=Answer_ID)

                        return jsonify({"message": update, "Updated answer": updated_answer})
                return make_response(jsonify({"message": "Answer doesnt exist"}), 400)
            return make_response(jsonify({"message": "Question doesnt exist"}), 400)
        except Exception as e:
            print(e)
            return {'Message': 'Please check your Question or Answer'}


api.add_resource(AnswerList, '/api/v1/questions/<string:Question_ID>/answers')
api.add_resource(
    Answers, '/api/v1/questions/<string:Question_ID>/answers/<string:Answer_ID>')
