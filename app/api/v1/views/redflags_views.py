from flask import request
from flask_restful import Resource
from ..models.redflags_models.py import Find


class RedFlags(Resource):
    def get(self):
        redflags = Find().all()
        return redflags

    def post(self):
        new_post = Find().new()
        return new_post


class RedFlagsSpecific(Resource):
    def get(self, flag):
        specific_red_flag = Find().specific()
        return specific_red_flag

    def put(self, modify):
        new_red_flag = Find().modification()
        return new_red_flag
