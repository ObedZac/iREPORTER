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
        self.token = data.get("token")


        return self.token

    def post_incident(self, data):
        """
            post an incident
        """
        token = self.get_jwt_token()
        
        incident = self.app.post('/api/v2/incidences/',
                                data=json.dumps(data),
                                headers={'content-type': 'application/json',
                                         'Authorization': 'Bearer ' + token})

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
                                         'Authorization': 'Bearer ' + token})
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
                                         'Authorization': 'Bearer ' + token})
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
                                         'Authorization': 'Bearer ' + token})
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
                                         'Authorization': 'Bearer ' + token})
        return incident

    def test_post_incident(self):
        """Test for posting an incident"""
        response = self.post_incident(self.red_flag2)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['data'][0]['message'], 'redflag record created Successfully.')
    
    def test_missing_token(self):
        """Test for posting an incident"""
        response = self.app.post('/api/v2/incidences/',
                                data=json.dumps(self.red_flag3),
                                headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data())
        self.assertEqual(data['msg'], 'Missing Authorization Header')

    def test_new_incident_no_title(self):
        """Test for posting a redflag without title"""
        response = self.post_incident(self.redflag_no_title)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['error'],"Title is invalid or empty")

    def test_new_incident_no_comment(self):
        """Test for posting a redflag without a body"""
        response = self.post_incident(self.redflag_no_comment)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['error'], 'description is invalid or empty')
    
    def test_new_incident_invalid_image(self):
        """Test for posting a redflag without a valid link image"""
        response = self.post_incident(self.redflag_invalid_image)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        print(data)
        self.assertEqual(data['error'], 'Images link is invalid')

    def test_new_incident_invalid_video(self):
        """Test for posting a redflag without a valid link video"""
        response = self.post_incident(self.redflag_invalid_video)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['error'], 'Video link is invalid')

    def test_view_all_incidents(self):
        """Test for viewing all incidents"""
        self.get_jwt_token()
        token = self.token
        self.post_incident(self.red_flag)
        response = self.app.get('/api/v2/incidences/',
                                headers={'content-type': 'application/json',
                                         'Authorization': 'Bearer ' + token})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "All incidents found successfully")

    def test_view_an_incident(self):
        """Test for vieving a particular redflag"""
        self.get_jwt_token()
        token = self.token
        self.post_incident(self.red_flag)
        response = self.app.get('/api/v2/incidences/1/',
                                    headers={'content-type': 'application/json',
                                         'Authorization': 'Bearer ' + token})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Incident successfully retrieved!")

    def test_view_incident_not_found(self):
        """Test for viewing an incident that does not exist"""
        self.get_jwt_token()
        token = self.token
        response = self.app.get('/api/v2/incidences/112/',
                                    headers={'content-type': 'application/json',
                                         'Authorization': 'Bearer ' + token})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data())
        self.assertEqual(data['error'], "Incident not found")

    def test_delete_an_incident(self):
        """Test for deleting a redflag"""
        self.post_incident(self.red_flag)
        self.get_jwt_token()
        token = self.get_jwt_token()
        response = self.app.delete('/api/v2/incidences/1/',
                                    headers={'content-type': 'application/json',
                                         'Authorization': 'Bearer ' + token})
        print(response.get_json())
        self.assertEqual(response.status_code, 200)

    def test_delete_incident_not_found(self):

        self.post_incident(self.red_flag)
        token = self.token
        response = self.app.delete('/api/v2/incidences/112/',
                                    headers={'content-type': 'application/json',
                                         'Authorization': 'Bearer ' + token})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data())
        self.assertEqual(data['error'], "Incident not found")

    def test_update_incident(self):
        """Test for updating an incident"""
        self.post_incident(self.red_flag2)
        response = self.put_incident(self.update_redflag)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Incident updated successfully!')

    def test_update_incident_no_title(self):
        """Test for updating an incident"""
        self.post_incident(self.red_flag2)
        response = self.put_incident( self.redflag_no_title)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['error'], 'Title is invalid or empty')

    def test_update_incident_no_image(self):
        """Test for updating an incident"""
        self.post_incident(self.red_flag2)
        response = self.put_incident( self.redflag_invalid_image)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['error'], 'Images link is invalid')

    def test_update_incident_no_location(self):
        """Test for updating an incident"""
        self.post_incident(self.red_flag2)
        response = self.put_incident( self.redflag_invalid_location )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['error'], 'location input is invalid')

    def test_update_incident_no_comment(self):
        """Test for updating an incident"""
        self.post_incident(self.red_flag2)
        response = self.put_incident( self.redflag_no_comment )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['error'], 'description is invalid or empty')
