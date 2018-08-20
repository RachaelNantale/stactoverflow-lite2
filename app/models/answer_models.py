import datetime
import uuid


class AnswersModels:
    def __init__(self, answer):
        self.id = uuid.uuid4().hex
        self.answer = answer
        self.time = datetime.datetime.now()

    def to_answerjson(self):
        """
        json representation of the answers model
        """
        return {
            'id': self.id,
            'answer': self.answer,
            'time': self.time
        }
