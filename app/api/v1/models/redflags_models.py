"""Models class for incidence creation"""
from flask import request

redflags = []


class Incident():
    """class containing methods for incidences manipulation"""

    def __init__(self):
        """Method for initializing incidences storage"""
        self.db = redflags

    def all(self):
        """Method for getting all the redflags"""
        return self.db

    def new(self, payload):
        """Method for posting new incidence"""
        self.db.append(payload)
        return self.db

    def specific(self, id):
        """Method for getting a specific incidence"""
        for redflag in redflags:
            if redflag["id"] == id:
                return redflag
            # return None

    def modification(self, id, **kwargs):
        """Method for modifying a specic incidence"""
        for redflag in redflags:
            if redflag["id"] == id:
                redflag["title"] = request.json["title"]
                redflag["type"] = request.json["type"]
                redflag["images"] = request.json["images"]
                redflag["video"] = request.json["video"]
                redflag["location"] = request.json["location"]
                redflag["comment"] = request.json["comment"]
                redflag["status"] = request.json["status"]
                return redflag
        return None

    def delete_redf(self, id):
        """Method for deleting a specific incidence"""
        for redflag in redflags:
            if redflag["id"] == id:
                redflags.remove(redflag)
                return redflag
        return None
