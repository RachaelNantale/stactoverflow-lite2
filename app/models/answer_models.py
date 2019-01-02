import datetime
import uuid
from app.utilities.utilities import validate_answer_input
from DBHandler import MyDatabase

db = MyDatabase()


class AnswersModels:
    """Answer model defines the parameters used in the Answer view.
    param: Question_ID  - Defines the ID of the questio to which the answer belongs to
    param: Answer_ID -  unique identifier of the answer
    Param: answer - this is the body or description of the answer
    Param: answered_by - defines the owner of the answer
    Param created_ at Time of creation"""
    def __init__(self, answer, Question_ID, answered_by):
        self.Question_ID = Question_ID
        self.answer = answer.strip(" ")
        self.answered_by = answered_by
        self.created_at = datetime.datetime.now()

    def to_answerjson(self):
        """
        json representation of the answers model
        """
        return {
            'answer': self.answer,
            'Created At': self.created_at
        }

    def create_answer(self):
        """This method checks if the answer exists before creating the answer"""
        if db.check_answer_exists(self.Question_ID, self.answer):
            return {'message': 'Answer already exists'}, 400

        validate = validate_answer_input(self.answer)
        if validate:
            return validate

        sql = "INSERT INTO AnswerTable values('{}','{}','{}', '{}')".format(
             self.created_at, self.answer, self.Question_ID,
            self.answered_by)
        return db.create_item(sql)
