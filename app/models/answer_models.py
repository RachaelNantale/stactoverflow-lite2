import datetime
import uuid


class AnswersModels:
    def __init__(self, body):
        self.body = body
        self.time = datetime.datetime.now()
        self.id = uuid.uuid4().hex

    def to_answerjson(self):
        """
        json representation of the answers model
        """
        return {'id': self.body,
                'title': self.time,
                'body': self.id

                }
