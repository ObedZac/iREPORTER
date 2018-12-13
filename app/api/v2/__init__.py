from flask import Blueprint
from flask_restful import Api
from .views.users_views import Login, Register

version_two = Blueprint("v2", __name__, url_prefix="/api/v2")
API = Api(version_two)


API.add_resource(Login, '/auth/login/')
API.add_resource(Register, '/auth/register/')

 
