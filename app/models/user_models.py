import uuid
from flask_bcrypt import Bcrypt
from DBHandler import MyDatabase

db = MyDatabase()


class UserModel():

    def __init__(self, email, password):
        self.User_ID = uuid.uuid4().hex
        self.email = email.strip(" ")
        self.password = password.strip(" ")

    def create_user(self):
        sql = "INSERT INTO UserTable values('{}','{}','{}')RETURNING User_ID".format(
            self.User_ID, self.email, self.password)
        db.create_login(sql)

    def fetch_user(self):
        sql = "SELECT * FROM UserTable WHERE email = '{}'".format(
            self.email)
        db.fetch_user(sql)

    
