import datetime
import uuid
from app.utilities.utilities import validate_answer_input
from DBHandler import MyDatabase

db = MyDatabase()


class AnswersModels:
    def __init__(self, answer, Question_ID, answered_by):
        self.Question_ID = Question_ID
        self.Answer_ID = uuid.uuid4().hex
        self.answer = answer.strip(" ")
        self.answered_by = answered_by
        self.created_at = datetime.datetime.now()

    def to_answerjson(self):
        """
        json representation of the answers model
        """
        return {
            'id': self.Answer_ID,
            'answer': self.answer,
            'Created At': self.created_at
        }

    def create_answer(self):
        if db.check_answer_exists(self.Question_ID, self.answer):
            return {'Message': 'Answer already exists'}, 400

        validate = validate_answer_input(self.answer)
        if validate:
            return validate

        sql = "INSERT INTO AnswerTable values('{}','{}','{}','{}', '{}')".format(
            self.Answer_ID, self.created_at, self.answer, self.Question_ID,
            self.answered_by)
        return db.create_item(sql)
