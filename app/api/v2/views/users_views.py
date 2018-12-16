import datetime
from flask import jsonify
from flask_restful import Resource, reqparse, request
from app.api.v2.models.users_models import Users
from flask_jwt_extended import create_access_token
from app.api.v2.validators.validators import Validation

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
        args = parser.parse_args()
        valid = Validation()

        username = args.get('username').strip()
        password = args.get('password').strip()

        if not request.json:
            return jsonify({"error" : "check your request type"})

        if not valid.valid_string(username) or not bool(username) :
            return {"error" : "Username is invalid or empty"}, 400

        if not valid.valid_password(password) or not bool(password):
            return {
                "error" : "Password should contain atleast 6 characters, a letter,\
                    an uppercase, a number and a special character"}, 400
        user = Users().find_by_name(args["username"])
        if user and user.verify(password=args["password"]):
            expire_time = datetime.timedelta(minutes=100)
            token = create_access_token(user.id,
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

    parser.add_argument('firstname', type=str, required=False, default="",
                        help='This field cannot be left blank!')

    parser.add_argument('lastname', type=str, required=False, default="",
                        help='This field cannot be left blank!')
                        
    parser.add_argument('email', type=str, required=True, default="",
                        help='This field cannot be left blank!')

    parser.add_argument('phoneNumber', type=int, required=False, default="",
                        help='This field cannot be left blank!')

    def post(self):
        """Post method to register a new user"""
        args = parser.parse_args()
        valid = Validation()
        username = args.get('username').strip()
        email    = args.get('email').strip()
        password = args.get('password').strip()
        if not request.json:
            return jsonify({"error" : "check your request type"})
        if not email or not valid.valid_string(username) or not bool(username) :
            return {"error" : "username is invalid or empty"}, 400
        if not valid.valid_email(email) or not bool(email):
            return {"error" : "email is invalid or empty!"}, 400
        if not valid.valid_password(password) or not bool(password):
            return {"error" : "Password should contain atleast 6 characters, a letter,\
                    an uppercase, a number and a special character"}, 400
        if Users().find_by_name(args["username"]) or Users().find_by_email(args["email"]):

            return {"status": 400,
                    "data": [{
                        "message": "Username or email already exists"
                    }]}, 400
        user = Users(**args)
        user.save_to_db()

        return {"status": 201,
                "data": [
                    {
                        "username": user.username,
                        "registered": user.registered
                    }],
                "message": 'Your user profile has been created Succesfully.'
                }, 201
