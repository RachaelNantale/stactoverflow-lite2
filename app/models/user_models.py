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

    # def create_user(self):
    #     sql = "INSERT INTO UserTable values('{}','{}','{}')RETURNING User_ID".format(
    #         self.User_ID, self.email, self.password)
    #     db.create_user(sql)

    # def fetch_user(self):
    #     sql = "SELECT * FROM UserTable WHERE email = '{}'".format(
    #         self.email)
    #     db.fetch_user(sql)

    # def check_user_exists(self):
    #     query = "SELECT * FROM UserTable WHERE email = '{}'".format(self.email)
    #     return db.check_user_exists(query)

    def create_user(self):
        validate = validate_user_input(self.email, self.password)
        if validate:
            return validate

        query = "SELECT * FROM UserTable WHERE email = '{}'".format(self.email)

        if db.check_user_exists(query):
            return {'Message': 'User already exists'}

        sql = "INSERT INTO UserTable values('{}','{}','{}')".format(
            self.User_ID, self.email, self.password)
        print(sql)
        return db.create_user(sql)

    def fetch_user(self, username):
        if validate_user_input(self.email, self.password):
            sql = "SELECT * FROM UserTable WHERE email = '{}'".format(
                self.email)
            # print(sql)
            return db.fetch_user(sql)
        return False


# def validate_user_input(self, email, password=None):

#     if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
#         return {'message': 'Please input a valid email'}, 400
#     if len(password) < 5:
#         return {'message': 'This password is not strong enough '}, 400
