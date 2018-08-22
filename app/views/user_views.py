import datetime
from flask import Flask, make_response, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import create_access_token
from app.models.user_models import UserModel
user_bp = Blueprint('app_users', __name__)
api = Api(user_bp)

Users = []


class Signup(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str,
                                   required=True, help='no email provided',)
        self.reqparse.add_argument('password', type=str,
                                   required=True, help='no password provided')
        super(Signup, self).__init__()

    def post(self):
        """
        Allows users to create accounts
        """
        args = self.reqparse.parse_args()
        new_user = UserModel(args['email'], args['password'])
        Users.append(new_user)
        return make_response(jsonify({'message': 'User succesfully created'}), 201)


class Login(Resource):
    """Login class"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str,
                                   required=True, help='no email provided',)
        self.reqparse.add_argument('password', type=str,
                                   required=True, help='no password provided')
        super(Login, self).__init__()

    def post(self):
        """
        Allows users to login to their accounts
        """
        args = self.reqparse.parse_args()

        for user in Users:
                if user.email == args['email'] and user.password == args['password']:
                    expires = datetime.timedelta(days=1)
                    access_token = create_access_token(identity=args['email'],
                                                       expires_delta=expires)
                    print(access_token)
                    return make_response(jsonify({'message': 'user successful\
                                                logged in',
                                                  'token': access_token}), 200)
                return make_response(jsonify({'message': 'Please check your email or password'}), 400)
        return make_response(jsonify({'message': 'User doesnot exist'}), 400)


api.add_resource(Signup, '/api/v1/auth/signup')
api.add_resource(Login, '/api/v1/auth/login')
