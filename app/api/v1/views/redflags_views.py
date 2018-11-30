from flask import request
from flask_restful import Resource
from ..models.redflags_models import Find


class RedFlags(Resource):

    def __init__(self):
        pass

    def get(self):
        redflags = Find().all()
        return redflags

    def post(self):
        new_post = Find().new()
        return new_post


class RedFlagsSpecific(Resource):

    def __init__(self):
        pass

    def get(self, id):
        specific_red_flag = Find().specific(id)
        return specific_red_flag

    def put(self, id):
        new_red_flag = Find().modification(id)
        return new_red_flag

    def delete(self, id):
        delete_flag = Find().delete_redf(id)
        return delete_flag
