import uuid
from DBHandler import MyDatabase
from app.utilities.utilities import validate_user_input
db = MyDatabase()


class UserModel():

    def __init__(self, email, password):
        self.User_ID = uuid.uuid4().hex
        self.email = email.strip(" ")
        self.password = password.strip(" ")

    def create_user(self):
        """This method creates a user. It first checks
        if the user already exists in the database in order to prevent
        duplication"""

        if db.fetch_user_by_email(self.email):
            return {'message': 'User already exists'}, 400

        validate = validate_user_input(self.email, self.password)
        if validate:
            return validate

        sql = "INSERT INTO UserTable values('{}','{}','{}')".format(
            self.User_ID, self.email, self.password)
        return db.create_item(sql)

    def fetch_user(self, email, password):
        """This method fetches the user in the database by
        email if they exist"""
        validate = validate_user_input(self.email, self.password)
        if validate:
            return validate

        sql = "SELECT * FROM UserTable WHERE email = '{}' and password = '{}'".format(
            self.email, self.password)
        return db.fetch_user(sql)
