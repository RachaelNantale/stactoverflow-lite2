import datetime
from flask import Flask, make_response, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import create_access_token
from app.models.user_models import UserModel
user_bp = Blueprint('app_users', __name__)
api = Api(user_bp)


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
        response = UserModel(args['email'], args['password'])
        print(response)
        try:

            created_user = response.create_user()
            return created_user

        except Exception:
            created_user = response.create_user()
            status_code = 400
            return make_response(jsonify({'User': created_user}), status_code)


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
        user = UserModel(args['email'], args['password'])
        logged_in_user = user.fetch_user(args['email'])

        if logged_in_user is not None:
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=args['email'],
                                               expires_delta=expires)
            return make_response(jsonify({'message': 'user successful logged in',
                                          'token': access_token}))

        return make_response(jsonify({'message': 'User not found.Please sign up'}), 400)


api.add_resource(Signup, '/api/v1/auth/signup')
api.add_resource(Login, '/api/v1/auth/login')
