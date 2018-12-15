"""Models class for users."""
import datetime
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

users = []


class Users():
    """class containing methods for users manipulation"""

    id = 0

    def __init__(self, firstname=None,
                 lastname=None,
                 email=None,
                 phonenumber=None,
                 username=None,
                 password=None):
        """Method for initializing users storage"""
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = self.generate_pass_hash()
        self.phoneNumber = phonenumber
        self.username = username
        self.created_on = datetime.datetime.now().strftime('%c')
        self.db = users

        Users.id += 1

    @staticmethod
    def generate_pass_hash():
        """ encrypt password"""

        private_key = generate_password_hash(request.json["password"])
        return private_key

    def verify(self, password=""):
        """
        Ensure user is authenticated and check their password.

        :param: password: verify given password
        :type password: str
        :returns verified password
        """
        return check_password_hash(self.password, password)

    def find_by_id(self, id):
        """Method for find user by id"""
        for user in self.db:
            if user["id"] == id:
                return user
            return None

    @staticmethod
    def find_by_name(username):
        """Method for find user by username"""
        for user in users:
            if user.username == username:
                return user
        return None

    @staticmethod
    def find_by_email(email):
        """Method for find user by email"""
        for user in users:
            if user.email == email:
                return user
        return None

    def save_to_db(self):
        """Method for saving user to database."""
        self.db.append(self)
