from flask-restful import reqparse
Redflags = []
class Find():
    def all(self):
        return {"status":200, "data":Redflags}
    def new(self): 
        self.parser = reqparse.RequestParser()
        args = self.parser.parse_args()
        Redflag = {
            "id" : len(Redflags)+1,
            "createdon" : datetime.now,
            "createdby" : args["user"],
            "type" : args["type"],
            "title": args["title"],
            "images": args["image"],
            "video": args["video"],
            "location": args["location"],
            "status" : "pending",
            "description" : args["description"]
        }
        Redflags.append(Redflag)
        return {"status": 201, "data":Redflag}
    def specific(self, flag):
        for Redflag in Redflags
            if Redflag["id"] == flag:
                return {"status":200,"data": Redflag}
            else:
                return{"status":404' "data": 'Redflag not found}

         