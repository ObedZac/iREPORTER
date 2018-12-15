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


class Incidents(Resource):
    """
    Fetch a all red-flag record.
    Create a red-flag record.

    :param: incident:
            {
              “id” : Integer,
              “type” : String,       // [red-flag, intervention]
              “location” : String,   // Lat Long coordinates
              “status” : String,     // [draft,
              under investigation, resolved, rejected]
              “Images” : [Image, Image],
              “Videos” : [Image, Image],
              “comment” : String
            }
    :returns records and success massage in json format.
    """
    @jwt_required    
    def get(self):
        """
            This method retrives all the posted incidents from the database
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
        data = parser.parse_args()
        new_record = Incident(createdBy="createdBY", **data)
        new_record.save_to_db()

        return {"status": 201,
                "data": [{
                    "message": "{} record created "
                               "Successfully.".format(new_record.record_type)
                }]}, 201
