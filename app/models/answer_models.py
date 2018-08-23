import datetime
import uuid


class AnswersModels:
    def __init__(self, answer):
        self.Answer_ID = uuid.uuid4().hex
        self.answer = answer.strip(" ")
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
