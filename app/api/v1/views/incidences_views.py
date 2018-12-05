"""Views for Incidences"""
import datetime
from flask import request
from flask_restful import Resource, reqparse
from ..models.incidences_models import Incident, redflags

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True, help="Field required.")
parser.add_argument("type", type=str, required=False, help="Field required.")
parser.add_argument("location", type=str, required=True,
                    help="Field required.")
parser.add_argument("images", type=str, required=False, help="Field required.")
parser.add_argument("video", type=str, required=False, help="Field required.")
parser.add_argument("status", type=str, required=False, help="Field required.")
parser.add_argument("comment", type=str, required=True, help="Field required.")


class RedFlags(Resource, Incident):
    """Path for get all incidences and posting a new one"""

    def __init__(self):
        """Initialize the redflags storage"""
        self.db = redflags

    def get(self):
        """Get all the incidences method"""
        redflags = self.all()
        return {"status": 200, "data": redflags, 'message': 'All redflags found successfully'}

    def post(self):
        """Post a new incidence method"""
        data = parser.parse_args()
        id = len(redflags)+1
        title = data['title']
        flag_type = data['type']
        location = data["location"]
        created_on = datetime.datetime.now().strftime('%c')
        image = data["images"]
        video = data["video"]
        comment = data["comment"]
        status = data["status"]
        payload = {
            "id": id,
            'created_on': created_on,
            'title': title,
            'type': flag_type,
            'location': location,
            'images': image,
            'video': video,
            'comment': comment,
            'status': status
        }
        errors = []

        if title == "" or title.isspace() or not title.isalpha():
            errors.append(
                {"title": "Title field can not be empty, numbers only  or contain special characters."})
        if location == "" or location.isspace() or not location.isalpha():
            errors.append(
                {"location": "Location field can not be empty, numbers only  or contain special characters."})
        if comment == "" or comment.isspace() or not comment.isalpha():
            errors.append(
                {"comment": "Comment field can not be empty, numbers only  or contain special characters."})

        if errors:
            return {
                "errors": errors
            }

        new_post = self.new(payload)
        return {"status": 201, "data": new_post[-1], 'message': 'redflag posted successfully!'}, 201


class RedFlagsSpecific(Resource, Incident):
    """Path for get specific, update and delete a post"""

    def get(self, id):
        """Get a specific incidence method"""
        specific_red_flag = self.specific(id)
        if specific_red_flag:
            return {"status": 200, "data": specific_red_flag,
                    "message": "redflag successfully retrieved"}, 200
        return {"status": 404, "data": "not found"}, 404

    def put(self, id):
        """Edit a specific incidence method"""
        payloads = {
            "title": request.json["title"],
            "type": request.json["type"],
            "location": request.json["location"],
            "images": request.json["images"],
            "video": request.json["video"],
            "comment": request.json["comment"],
            "status": request.json["status"]
        }
        new_red_flag = self.modification(id, **payloads)
        if new_red_flag:
            return {"status": 200, "data": new_red_flag,
                    'message': 'redflag updated successfully!'}, 200
        return {"status": 404, "data": "not found"}, 404

    def delete(self, id):
        """Delete a spcific incidence method"""
        delete_flag = self.delete_redf(id)
        if delete_flag:
            return {"status": 200, 'message': 'redflag successfuly deleted'}
        return {"status": 404, "data": "not found"}, 404
