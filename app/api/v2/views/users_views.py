import datetime
from flask import jsonify
from flask_restful import Resource, reqparse, request
from app.api.v2.models.users_models import Users
from flask_jwt_extended import create_access_token

parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('username', type=str, required=True,
                    help='This field cannot be left blank!')
parser.add_argument('password', type=str, required=True,
                    help='This field cannot be left blank!')


class Login(Resource):
    """
    Authorize a user to access the data.

    :param user:{ “username” : String,
                  “password” : String,
                }
    :returns verified user
    """
    def post(self):
        """
        Receives data in json format and authenticates the user is exists

        :return: Jwt token and success status
        """
        request_data = parser.parse_args()
        user = Users().find_by_name(request_data["username"])
        if user and user.verify(password=request_data["password"]):
            expire_time = datetime.timedelta(minutes=20)
            token = create_access_token(user.username,
                                        expires_delta=expire_time)
            return {"status": 200,
                    'token': token,
                    "data": [{
                        'message': f'Login successful.'
                        f' Welcome {user.username}. You are logged in as user'
                        f' ID {user.id}.'
                    }]}, 200

        return {"status": 400,
                "data": [{
                    "message": "User doesn't exists, kindly register a new account."
                }]}, 400


class Register(Resource):
    """
    Authorize a user to access register a new account.

    :param user:{ “username” : String,
                  “password” : String,
                  “firstname” : String,
                  “lastname” : String,
                  “username” : String,
                  “email” : String,
                  “phonenumber” : Integer
                }
    :returns new user account.
    """

    parser.add_argument('firstname', type=str, required=True, default="",
                        help='This field cannot be left blank!')

    parser.add_argument('lastname', type=str, required=True, default="",
                        help='This field cannot be left blank!')
                        
    parser.add_argument('email', type=str, required=True, default="",
                        help='This field cannot be left blank!')

    parser.add_argument('phoneNumber', type=int, required=True, default="",
                        help='This field cannot be left blank!')

    def post(self):
        """Post method to register a new user"""
        request_data = parser.parse_args()

        if Users().find_by_name(request_data["username"]) or Users().find_by_email(request_data["email"]):

            return {"status": 400,
                    "data": [{
                        "message": "Username or email already exists"
                    }]}, 400
        user = Users(**request_data)
        user.save_to_db()

        return {"status": 201,
                "data": [
                    {
                        "username": user.username,
                        "registered": user.registered
                    }],
                "message": 'Your user profile has been created Succesfully.'
                }, 201
