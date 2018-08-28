import datetime
import uuid
import re

from DBHandler import MyDatabase

db = MyDatabase()


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

    def create_question(self):
        if validate_question_input(self.title, self.description,
                                   self.tags):
            sql = "INSERT INTO QuestionTable values('{}','{}','{}','{}','{}')RETURNING Question_ID".format(
                self.Question_ID, self.title, self.description, self.tags,
                self.time)
            result = db.create_user(sql)
            return result
        return False

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


def validate_question_input(title, description, tags):
    """ Function to validate data entered while creating a question """
    if len(title) < 5 or title == "" or title == " ":
        return {'message': 'Title is too short. Please add more clarity'}, 400
    if re.compile('[!@#$%^&*:;?><.]').match(title):
        return {'message': 'Please dont input symbols'}, 400

    if len(description) < 5 or description == " ":
        return {'message': 'Description is too short.'}, 400
    if re.compile('[!@#$%^&*:;?><.]').match(description):
        return {'message': 'Please dont input symbols'}, 400

    if not tags or tags == "":
        return {'message': 'Please a correct tag'}, 400
    if re.compile('[!@#$%^&*:;?><.]').match(tags):
        return {'message': 'Please dont input symbols'}, 400
    return QuestionsModels(title=title, description=description,
                           tags=tags)
