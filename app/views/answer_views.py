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
                return make_response(jsonify(question), 200)
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

        args = self.reqparse.parse_args()
        current_user = get_jwt_identity()
        user = db.fetch_user_by_email(email=current_user)
        logged_in_user = user
        print(logged_in_user)

        answer_exists = db.fetch_answer_by_id(Answer_ID=Answer_ID)
        question_exists = db.fetch_single_question_by_id(
            Question_ID=Question_ID)
        a_owner = db.fetch_answer_details(Question_ID, Answer_ID)
        qtn_details = db.fetch_a_question(Question_ID=Question_ID)

        if question_exists:
            if answer_exists:
                if logged_in_user == a_owner:
                    my_answer = AnswersModels(
                        args['answer'], Question_ID, logged_in_user)
                    update = db.update_answer(
                        answer=args['answer'], Question_ID=Question_ID,
                        Answer_ID=Answer_ID)
                    updated_answer = db.fetch_answer_details(
                        Question_ID=Question_ID, Answer_ID=Answer_ID)
                    return {'msg': update, 'upt_ans': updated_answer}
                if logged_in_user == qtn_details:
                    status = True

                    accept = db.accept_answer(
                        status=status, Question_ID=Question_ID, Answer_ID=Answer_ID)
                    updated_answer = db.fetch_answer_details(
                        Question_ID=Question_ID, Answer_ID=Answer_ID)
                    return jsonify({"message": accept, "Updated answer": updated_answer})
            return make_response(jsonify({"message": " No such answer exists"}), 400)
        return make_response(jsonify({"message": " No such question exists any more"}), 400)


api.add_resource(AnswerList, '/api/v1/questions/<string:Question_ID>/answers')
api.add_resource(
    Answers, '/api/v1/questions/<string:Question_ID>/answers/<string:Answer_ID>')
