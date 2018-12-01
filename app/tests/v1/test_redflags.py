"""Test for methods applied to Red Flags"""
import json
from .base import BaseTestCase


class TestRequestsTestCase(BaseTestCase):
    """Tests for Questions"""

    def create_incident(self):
        response = self.client().post('api/v1/redflags', data=json.dumps(
            self.red_flag), headers={'content-type': "application/json"})
        return response

    def test_new_redflag(self):
        """Test for posting a redflag"""
        #correct request
        response = self.create_incident()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Redflag posted successfully!')

    # def test_new_redflag_no_title(self):
    #     """Test for posting a redflag without title"""
    #     #no title
    #     response = self.client().post('api/v1/redflags', data=json.dumps(
    #         self.redflag_no_title), headers={'content-type': "application/json"})
    #     self.assertEqual(response.status_code, 200)
    #     # data = json.loads(response.get_data())
    #     data = response.get_json()
    #     self.assertEqual(data['message'], 'Title is required')

    # def test_new_redflag_no_comment(self):
    #     """Test for posting a redflag without a body"""
    #     #no body
    #     response = self.client().post('/ireporter/api/v1/red-flags/', data=json.dumps(
    #         self.redflag_no_comment), headers={'content-type': "application/json"})
    #     self.assertEqual(response.status_code, 201)
    #     data = json.loads(response.get_data())
    #     self.assertEqual(data['message'], 'Body is required')

    def test_view_all_redflags(self):
        """Test for viewing all redflags"""
        response = self.client().get('api/v1/redflags')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "All redflags found successfully")

    def test_view_a_redflag(self):
        """Test for viewing a particular redflag"""
        #existing redflag
        response = self.client().get('api/v1/redflags/2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Redflag successfully retrieved")

    def test_view_reflag_not_found(self):
        """Test for viewing a redflag that does not exist"""
        #redflag does not exist
        response = self.client().get('api/v1/redflags/1')
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
        # self.assertIn("Redflag updated successfully!", data["message"])
        self.assertDictEqual({"status": 200,
                              "data": {
                                  "id": self.update_redflag["id"],
                                  "title": self.update_redflag["title"],
                                  "type": self.update_redflag["type"],
                                  "location": self.update_redflag["location"]
                              },
                              "message": "Redflag updated successfully!"
                              }, data)

    def test_modify_a_redflag_not_found(self):
        """Test for modifying a redflag not found"""
        response = self.client().put(f'api/v1/redflags/2',
                                     data=json.dumps(self.update_redflag),
                                     headers={'content-type': "application/json"})
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 404)
        # self.assertIn("Redflag updated successfully!", data["message"])
        self.assertDictEqual({'data': 'not found', 'status': 404}, data)

    def test_user_delete_a_question(self):
        """Test for deleting a redflag"""
        response = self.client().delete('api/v1/redflags/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Redflag successfuly deleted")
