"""This module holds the classes and methods for incidents views manipulation"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from app.api.v2.models.incidences_models import Incident


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('record_type',
                    type=str,
                    required=True,
                    choices=("redflag", "intervention"),
                    help="This field cannot be left "
                         "blank or Bad choice: {error_msg}"
                    )

parser.add_argument('location',
                    type=str,
                    required=True,
                    help="This field can be left blank!"
                    )

parser.add_argument('status',
                    type=str,
                    required=True,
                    choices=("rejected", "under investigation", "resolved", "deleted"),
                    help="This field cannot be left "
                         "blank or Bad choice: {error_msg}"
                    )
parser.add_argument('images',
                    action='append',
                    help="This field can be left blank!"
                    )
parser.add_argument('video',
                    action='append',
                    help="This field can be left blank!"
                    )

parser.add_argument('title',
                    action='append',
                    help="This field can be left blank!"
                    )

parser.add_argument('comment',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )


class Incidences(Resource):
    """
    Fetch all incidents records.
    Create a new incident record.

    :param: incident:
            {
              “id” : Integer,
              “type” : String,
              “location” : String,  
              “status” : String, 
              “Images” : [Image, Image],
              “Videos” : [Image, Image],
              “comment” : String
            }
    :returns records and success massage in json format.
    """
    @jwt_required    
    def get(self):
        """
            This method retrives all the posted incidents from database
        """
        self.model = Incident()
        if self.model.get_all_incidents():
            incidents = self.model.get_all_incidents()
            return {"status": 200,
                            "data": [{
                                "RedFlags": incidents
                            }],
                            "message": "All incidents found successfully"}, 200

    @jwt_required
    def post(self):
        """
            This method creates a new incident into the database
        """
        data = parser.parse_args()
        new_record = Incident(createdBy="createdBy", **data)
        new_record.save_to_db()

        return {"status": 201,
                "data": [{
                    "message": "{} record created "
                               "Successfully.".format(new_record.record_type)
                }]}, 201

class Incidence(Resource):
    """
        This class holds methods for single incident manipulation
    """
    @jwt_required
    def get(self, incident_id):
        """
            This method retrieves an incident from the database by using its id
        """
        self.model = Incident()
        incidence = self.model.find_incidence_by_id(incident_id)
        if not incidence:
            return {"status": 404, "error": "Incident not found"}, 404
        return {"status": 200,
                        "data": [
                            {
                                "redflag": incidence,
                            }
                        ],
                        "message": "Incident successfully retrieved!"}, 200
 
    @jwt_required
    def delete(self, incident_id):
        """
            This method removes an incident from the db
        """
        self.model = Incident()
        incident = self.model.find_incidence_by_id(incident_id)
        if not incident:
            return {"status": 404, "error": "Incident not found"}, 404


        inc = incident.get('createdBy')        
        user = self.model.current_user()
        if user != inc:
            return {'status': 403,"error": "This action is forbidden.",
            'message': ' You are trying to delete someone else post'}


        if self.model.delete_from_db():
            return {"status": 200, "message": "Incident successfuly deleted"}, 200


   