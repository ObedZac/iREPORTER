from flask import request
from flask-restful import resource
from app.api.v1.models.redflags_models import Find
class RedFlags(Resource):
    def get(self):
        redflags = Find().all()
        return redflags
    def post(self):
        new_post = Find().new()
        return new_post
        
