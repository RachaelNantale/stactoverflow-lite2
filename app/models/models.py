import datetime


class QuestionsModels:

    def __init__(self,  title, body, tags, Question_ID):
        self.Question_ID = Question_ID
        self.title = title
        self.body = body
        self.tags = tags
        self.answers = []
        self.time = datetime.datetime.now()

    def to_questionjson(self):
        """
        json representation of the questions model
        """
        return {
            'id': self.Question_ID,
            'title': self.title,
            'Description': self.body,
            'tags': self.tags
        }
