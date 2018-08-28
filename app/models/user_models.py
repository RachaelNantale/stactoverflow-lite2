import uuid
from flask_bcrypt import Bcrypt
from DBHandler import MyDatabase
import re
from app.utilities.utilities import validate_user_input
db = MyDatabase()


class UserModel():

    def __init__(self, email, password):
        self.User_ID = uuid.uuid4().hex
        self.email = email.strip(" ")
        self.password = password.strip(" ")

    def create_user(self):
        query = "SELECT * FROM UserTable WHERE email = '{}'".format(self.email)

        if db.check_user_exists(query):
            print(query)
            return {'Message': 'User already exists'}, 400

        validate = validate_user_input(self.email, self.password)
        if validate:
            return validate

        sql = "INSERT INTO UserTable values('{}','{}','{}')".format(
            self.User_ID, self.email, self.password)
        print(sql)
        return db.create_user(sql)

    def fetch_user(self, email):
        validate = validate_user_input(self.email, self.password)
        if validate:
            return validate

        sql = "SELECT * FROM UserTable WHERE email = '{}'".format(
            self.email)
        print(sql)
        return db.fetch_user(sql)
