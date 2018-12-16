"""Test for methods applied to Red Flags"""
import json
from app.tests.v2.base import BaseTestCase

class TestIncidentsTestCase(BaseTestCase):
    """Tests for incidents"""

    def signup(self):
        """ 
             create a test user 
        """
        response = self.app.post('/api/v2/auth/register/',
                                 data=json.dumps(self.person_existing_user),
                                 headers={'content-type': 'application/json'}
                                 )

        return response

    def login(self):
        """
            sign in a user
        """
        response = self.app.post('api/v2/auth/login/',
                                 data=json.dumps(self.correct_login1),
                                 headers={'content-type': 'application/json'})
        return response

    def get_jwt_token(self):
        """
            get jwt token
        """
        self.signup()
        t = self.login()
        data = json.loads(t.get_data())   
        self.data = data.get("data")[0]
        self.token = self.data.get('token')
        return self.token

    def post_incident(self, data):
        """
            post an incident
        """
        self.get_jwt_token()
        token = self.token
        incident = self.app.post('/api/v2/incidences/',
                                data=json.dumps(data),
                                headers={'content-type': 'application/json',
                                         'Authorization': token})
        return incident

    def put_incident(self, data):
        """
            post an incident
        """
        self.get_jwt_token()
        token = self.token
        incident = self.app.put('/api/v2/incidences/1/',
                                data=json.dumps(data),
                                headers={'content-type': 'application/json',
                                         'Authorization': token})
        return incident
    def patch_comment(self, id, data):
        """
            post an incident
        """
        self.get_jwt_token()
        token = self.token
        incident = self.app.patch('/api/v2/incidences/'+id+'/comment',
                                data=json.dumps(data),
                                headers={'content-type': 'application/json',
                                         'Authorization': token})
        return incident

    def patch_location(self, id, data):
        """
            post an incident
        """
        self.get_jwt_token()
        token = self.token
        incident = self.app.patch('/api/v2/incidences/'+id+'/location',
                                data=json.dumps(data),
                                headers={'content-type': 'application/json',
                                         'Authorization': token})
        return incident
    def patch_status(self, id, data):
        """
            post an incident
        """
        self.get_jwt_token()
        token = self.token
        incident = self.app.patch('/api/v2/incidences/'+id+'/status',
                                data=json.dumps(data),
                                headers={'content-type': 'application/json',
                                         'Authorization': token})
        return incident

    