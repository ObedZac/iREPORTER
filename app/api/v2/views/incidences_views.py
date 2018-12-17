"""This module holds the classes and methods for incidents views manipulation"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from app.api.v2.models.incidences_models import Incident
from app.api.v2.validators.validators import Validation


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
                    choices=("pending", "draft", "rejected",
                             "under investigation", "resolved", "deleted"),
                    help="This field cannot be left "
                         "blank or Bad choice: {error_msg}"
                    )
parser.add_argument('images',
                    type=str,
                    help="This field can be left blank!"
                    )
parser.add_argument('video',
                    type=str,
                    help="This field can be left blank!"
                    )

parser.add_argument('title',
                    type=str,
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
              “incident_id” : Integer,
              “record_type” : String,
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
        """This method retrives all the posted incidents from database"""
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
        """This method creates a new incident into the database"""
        valid = Validation()
        args = parser.parse_args()

        record_type = args.get("record_type")
        title = args.get("title")
        images = args.get("images")
        video = args.get("video")
        location = args.get("location")
        comment  = args.get("comment")

        if not request.json:
            return jsonify({"error" : "check your request type"})

        if not valid.valid_string(title) or not title.strip() :
            return {"error" : "Title is invalid or empty"}, 400

        if not valid.valid_string(images) :
            return {"error" : "Images link is invalid"}, 400

        if not valid.valid_string(video):
            return {"error" : "Video link is invalid"}, 400

        if not valid.valid_string(location):
            return {"error" : "location input is invalid"}, 400

        if not valid.valid_string(comment) or not comment.strip():
            return {"error" : "description is invalid or empty"}, 400

        if not record_type.strip() :
            return {"error" : "Type is invalid or empty"}, 400
        new_record = Incident(createdBy="createdBy", **args)
        new_record.save_to_db()

        return {"status": 201,
                "data": [{
                    "message": "{} record created "
                               "Successfully.".format(new_record.record_type)
                }]}, 201


class Incidence(Resource):
    """This class holds methods for single incident manipulation"""
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
    def put(self, incident_id):
        """This method allows editing of an incident partially or wholly"""
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("title",
                            type=str,
                            required=True,
                            help="title field is required.")
        parser.add_argument("comment",
                            type=str,
                            required=True,
                            help="comment field is required.")
        parser.add_argument("record_type",
                            type=str,
                            help="Type field is required.")
        parser.add_argument("images",
                            type=str,
                            help="images field is optional.")
        parser.add_argument("video",
                            type=str,
                            help="video field is optional.")
        parser.add_argument("location",
                            type=str,
                            help="location field is optional.")
        self.model = Incident()
        valid = Validation()
        args = parser.parse_args()
        record_type = args.get("record_type")
        title = args.get("title")
        images = args.get("images")
        video = args.get("video")
        location = args.get("location")
        comment = args.get("comment")

        if not request.json:
            return jsonify({"error" : "check your request type"})

        if not valid.valid_string(title) or not title.strip() :
            return {"error" : "Title is invalid or empty"}, 400

        if not valid.valid_string(images) :
            return {"error" : "Images link is invalid"}, 400

        if not valid.valid_string(video):
            return {"error" : "Video link is invalid"}, 400

        if not valid.valid_string(location):
            return {"error" : "location input is invalid"}, 400

        if not valid.valid_string(comment) or not comment.strip():
            return {"error" : "description is invalid or empty"}, 400

        if not record_type.strip() :
            return {"error" : "Type is invalid or empty"}, 400

        incident = self.model.find_incidence_by_id(incident_id)
        if not incident:
            return {"status": 404, "error": "Incindent not found"}, 404

        online = incident['createdby']
        user = self.model.current_user()
        if user != online:
            return {'status': 403, "error": "This action is forbidden.",
                    'message': 'You can only modify an incident that is yours!'}

        if not self.model.check_status(incident_id):
            return {'status': 403, "error": "This action is forbidden. Modify only a draft or pending incident."}

        if self.model.edit_incident(record_type, location, images, video, title, comment, incident_id):
            return {"status": 200,
                    "data": [
                        {
                            "incident": incident_id,
                        }
                    ],
                    "message": "Incident updated successfully!"}, 200

    @jwt_required
    def delete(self, incident_id):
        """This method removes an incident from the db"""
        self.model = Incident()
        incident = self.model.find_incidence_by_id(incident_id)
        if not incident:
            return {"status": 404, "error": "Incident not found"}, 404

        online = incident['createdby']
        user = self.model.current_user()
        if user != online:
            return {'status': 403, "error": "Action forbidden!",
                    'message': ' You can only delete an incident that is yours!'}

        elif self.model.delete_incident(incident_id):
            return {"status": 200, "message": "Incident deleted successfuly."}, 200


class IncidentLocation(Resource):
    """Class for a logged in user to patch the location."""
    @jwt_required
    def patch(self, incident_id):
        """method for a logged in user to patch the location"""
        data = parser.parse_args()
        self.model = Incident()
        incident = self.model.find_incidence_by_id(incident_id)

        if not incident:
            return {"status": 404,
                    "data": [{
                        "message": "Incident record Not Found."
                    }]}, 404

        online = incident['createdby']
        user = self.model.current_user()
        if user != online:
            return {'status': 403, "error": "Action forbidden!",
                    'message': ' You can only update location on an incident that is yours!'}

        if self.model.edit_location(data["location"], incident_id):
            return {
                "status": 202,
                "data": [{
                    "id": incident_id,
                         "message": "Location updated successfully"
                         }]
            }, 202


class IncidentComment(Resource):
    """Class for patching a comment."""
    @jwt_required
    def patch(self, incident_id):
        """method for a logged in user to patch a comment."""
        data = parser.parse_args()
        self.model = Incident()
        incident = self.model.find_incidence_by_id(incident_id)

        if not incident:
            return {"status": 404,
                    "data": [{
                        "message": "Incident record Not Found."
                    }]}, 404

        online = incident['createdby']
        user = self.model.current_user()
        if user != online:
            return {'status': 403, "error": "Action forbidden!",
                    'message': ' You can only update comment on an incident that is yours!'}

        if self.model.edit_comment(data["comment"], incident_id):
            return {
                "status": 202,
                "data": [{
                    "id": incident_id,
                         "message": "Comment updated successfully"
                         }]
            }, 202

class IncidentStatus(Resource):
    """Class for patching status."""
    @jwt_required
    def patch(self, incident_id):
        """method for a logged in user to patch status."""
        data = parser.parse_args()
        self.model = Incident()
        incident = self.model.find_incidence_by_id(incident_id)

        if not incident:
            return {"status": 404,
                    "data": [{
                        "message": "Incident record Not Found."
                    }]}, 404

        user = self.model.current_user()
        if user != 1 :
            return {'status': 403, 'error': 'you do not have permission to do that!'},403

        if self.model.edit_status(data["status"], incident_id):
            return {
                "status": 202,
                "data": [{
                    "id": incident_id,
                         "message": "Status updated successfully"
                         }]
            }, 202
