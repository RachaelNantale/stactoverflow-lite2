import datetime


class QuestionsModels:

    def __init__(self,  title, body, tags, qtn_id):
        self.qtn_id = qtn_id
        self.title = title
        self.tags = tags
        self.body = body
        self.answers = []
        self.time = datetime.datetime.now()

    def to_questionjson(self):
        """
        json representation of the questions model
        """
        return {
            'id': self.qtn_id,
            'title': self.title,
            'body': self.body,
            'tags': self.tags
        }
