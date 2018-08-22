import uuid


class UserModel():

    def __init__(self, email, password):
        self.User_ID = uuid.uuid4().hex
        self.email = email
        self.password = password
