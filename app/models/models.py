import datetime
import uuid


class QuestionsModels:

    def __init__(self,  title, description, tags):
        self.Question_ID = uuid.uuid4().hex
        self.title = title.strip("")
        self.description = description.strip(" ")
        self.tags = tags.strip(" ")
        self.answers = []
        self.time = datetime.datetime.now()

    def get_id(self):
        return self.Question_ID

    def to_questionjson(self):
        """
        json representation of the questions model
        """
        return {
            'id': self.Question_ID,
            'title': self.title,
            'Description': self.description,
            'tags': self.tags
        }
