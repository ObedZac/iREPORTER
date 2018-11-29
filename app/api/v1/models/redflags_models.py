from flask_restful import reqparse
import datetime
from flask import request, json, jsonify

Redflags = []

class Find():

    def __init__(self):
        self.db = Redflags

    def all(self):
        return jsonify({"status":200, "data":self.db})

    def new(self): 
        data = request.get_json()
        id = len(Redflags)+1
        title = data['title']
        flag_type = data['type']
        location = data["location"]
        # Redflag = {
        #     "createdon" : datetime.datetime.now(),
        #     "createdby" : args["createdby"],
        #     "type" : args["type"],
        #     "title": args["title"],
        #     "images": args["image"],
        #     "video": args["video"],
        #     "location": args["location"],
        #     "status" : "pending",
        #     "description" : args["description"]
        # }
        payload={
            'id': id,
            'title': title,
            'type' : flag_type,
            'location' : location
        }
        self.db.append(payload)
        return jsonify ({"status": 201, "data":self.db})

    def specific(self, id):
        for Redflag in Redflags:
            if Redflag["id"] == id:
                return {"status":200,"data": Redflags[0]}
            # else:
            #     return {"status":404, "data":"not found" }


    def modification(self, id):
        for Redflag in Redflags:
            if Redflag["id"] == id:
                Redflag["title"] = request.json["title"]
                Redflag["type"] = request.json["type"]
                # Redflag["images"] = request.json["images"]
                # Redflag["video"] = request.json["video"]
                Redflag["location"] = request.json["location"]
                # Redflag["description"] = request.json["description"]
                return {"status":204, "data": Redflag }
    def delete_redf(self, id):
        for Redflag in Redflags:
            if Redflag["id"] == id:
                Redflags.remove(Redflag)
                return {"status":204, "message":"Redflag successfuly deleted"}
                
