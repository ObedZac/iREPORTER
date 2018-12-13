"""Models class for users."""
import datetime
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from app.db_con import Database

class Users(Database):
    """class containing methods for users manipulation"""

    def __init__(self,
                 firstname=None,
                 lastname=None,
                 othernames=None,
                 email=None,
                 phoneNumber=None,
                 username=None,
                 password=None,
                 isAdmin=False):
        """Method for initializing users storage"""
        super().__init__('main')
        self.id=None
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.email = email
        self.password = Users.generate_pass_hash()
        self.phoneNumber = phoneNumber
        self.username = username
        self.registered = datetime.datetime.now().strftime('%c')
        self.isAdmin = isAdmin

    # def __repr__(self):
    #     """ Return repr(self). """
    #     return "{} in User Model.".format(self.username)

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

    def find_by_id(self, user_id):
        """Method for find user by id"""
        self.cur.execute("SELECT * FROM users "
                            "WHERE id=%s", (user_id,))
        user = self.fetch_one()
        self.save()

        if user:
            return self.mapping(user)
        return None

    def find_by_name(self, username):
        """Method for find user by username"""
        self.cur.execute("SELECT * FROM users "
                            "WHERE username=%s", (username,))
        user = self.fetch_one()
        self.save()

        if user:
            return self.mapping(user)
        return None

    def find_by_email(self, email):
        """Method for find user by email"""
        self.cur.execute("SELECT * FROM users "
                            "WHERE email=%s", (email,))
        user = self.fetch_one()
        self.save()

        if user:
            return self.mapping(user)
        return None
        
    def save_to_db(self):
        """Method for saving user to database."""
        query = """
                    INSERT INTO users (username, firstname, lastname,\
                    othernames, phoneNumber, email, password, isAdmin, registered)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        data = (self.username, self.firstname,
                self.lastname, self.othernames,
                self.phoneNumber, self.email,
                self.password, self.isAdmin,
                self.registered)

        self.cur.execute(query, data)
        self.save()

    def mapping(self, data):
        """ map user to user object"""
        print(data)
        self.id = data["user_id"]
        self.username = data["username"]
        self.password = data["password"]
        self.firstname = data["firstname"]
        self.lastname = data["lastname"]
        self.othernames = data["othernames"]
        self.email = data["email"]
        self.phoneNumber = data["phonenumber"]
        self.isAdmin = data["isadmin"]
        self.registered = data["registered"]

        return self
