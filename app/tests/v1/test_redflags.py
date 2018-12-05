"""Test for methods applied to Red Flags"""
import json
from .base import BaseTestCase


class TestRequestsTestCase(BaseTestCase):
    """Tests for questions"""

    def create_incident(self):
        """Initialize tests by creating a post"""
        response = self.client().post('api/v1/redflags', data=json.dumps(
            self.red_flag), headers={'content-type': "application/json"})
        return response

    def test_new_redflag(self):
        """Test for posting a redflag"""
        #correct request
        response = self.create_incident()
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'redflag posted successfully!'),201


    def test_view_all_redflags(self):
        """Test for viewing all redflags"""
        response = self.client().get('api/v1/redflags')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "All redflags found successfully")

    def test_view_a_redflag(self):
        """Test for viewing a particular redflag"""
        #existing redflag
        response = self.client().get('api/v1/redflags/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "redflag successfully retrieved")

    def test_view_reflag_not_found(self):
        """Test for viewing a redflag that does not exist"""
        #redflag does not exist
        response = self.client().get('api/v1/redflags/45')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data())
        self.assertEqual(data['data'], "not found")

    def test_modify_a_redflag_found(self):
        """Test for modifying a redflag found"""
        self.create_incident()
        response = self.client().put(f'api/v1/redflags/{self.update_redflag["id"]}',
                                     data=json.dumps(self.update_redflag),
                                     headers={'content-type': "application/json"})
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual({"status": 200,
                              "data": {
                                  "id": self.update_redflag["id"],
                                  "created_on" : self.update_redflag["createdOn"],
                                  "title": self.update_redflag["title"],
                                  "type": self.update_redflag["type"],
                                  "status" : self.update_redflag["status"],     
                                  "images" : self.update_redflag["images"], 
                                  "video" : self.update_redflag["video"],
                                  "comment" : self.update_redflag["comment"],
                                  "location": self.update_redflag["location"]
                              },
                              "message": "redflag updated successfully!"
                              }, data)

    def test_modify_a_redflag_not_found(self):
        """Test for modifying a redflag not found"""
        response = self.client().put(f'api/v1/redflags/2',
                                     data=json.dumps(self.update_redflag),
                                     headers={'content-type': "application/json"})
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 404)
        self.assertDictEqual({'data': 'not found', 'status': 404}, data)

    def test_user_delete_a_redflag(self):
        """Test for deleting a redflag"""
        response = self.client().delete('api/v1/redflags/2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "redflag successfuly deleted")

    def test_user_delete_a_redflag_not_found(self):
        """Test for deleting a redflag not found"""
        response = self.client().delete('api/v1/redflags/45')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertDictEqual({'data': 'not found', 'status': 404}, data)
