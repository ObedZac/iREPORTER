""" This module does validation for user input in the app """
import re

class Validation():
    """
        methods for validating user input data
    """

    def valid_email(self, email):
        """Validates the email"""
        self.validemail = re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
        if not self.validemail:
            return None
        return True

    def valid_password(self, password):
        """Validates the password"""
        self.password = re.match(r"^.*(?=.{6,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$*%^&+=]).*$", password)
        if self.password is None:
            return None
        return True

    def valid_string(self, value):
        """
            checks if value in data is empty
        """
        self.value = value
        return isinstance(self.value, str)
            