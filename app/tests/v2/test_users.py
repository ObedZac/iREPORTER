"""Tests for users"""
from .base import BaseTestCase
import json

class TestUsersTestCase(BaseTestCase):
    """
         test for users
    """
    def signup(self, user):
        """
             create a test user
        """
        response = self.app.post('/api/v2/auth/register/',
                                 data=json.dumps(user),
                                 headers={'content-type': 'application/json'}
                                 )

        return response

    def login(self, user):
        """
            sign in a user
        """
        response = self.app.post('api/v2/auth/login/',
                                 data=json.dumps(user),
                                 headers={'content-type': 'application/json'})
        return response

    
    def test_correct_signup(self):
        """
            test for signup with all required fields
        """
        response = self.signup(self.person)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        print(data)
        self.assertEqual(data['message'], 'Your user profile has been created Succesfully.')

    
