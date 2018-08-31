import datetime
import uuid
import re
from app.utilities.utilities import validate_question_input
from DBHandler import MyDatabase

db = MyDatabase()


class QuestionsModels:

    def __init__(self,  title, description, tags, asked_by):
        self.Question_ID = uuid.uuid4().hex
        self.title = title.strip(" ")
        self.description = description.strip(" ")
        self.tags = tags.strip(" ")
        self.asked_by = asked_by
        self.time = datetime.datetime.now()

    def get_id(self):
        return self.Question_ID

    def create_question(self):
        query = "SELECT * FROM QuestionTable WHERE title = '{}'".format(
            self.title)

        if db.check_item_exists(query):
            print(query)
            return {'Message': 'Question already exists'}, 400

        validate = validate_question_input(self.title, self.description,
                                           self.tags)
        if validate:
            return validate

        sql = "INSERT INTO QuestionTable values('{}','{}','{}','{}','{}','{}')".format(
            self.Question_ID, self.title, self.description, self.tags,
            self.asked_by, self.time)
        return db.create_item(sql)

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
