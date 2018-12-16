from flask import Blueprint
from flask_restful import Api
from .views.incidences_views import RedFlags, RedFlagsSpecific
from .views.users_views import Login, Register

version_one = Blueprint("v1", __name__, url_prefix="/api/v1")
API = Api(version_one)


API.add_resource(RedFlags, '/incidences')
API.add_resource(RedFlagsSpecific, '/incidences/<int:id>')
API.add_resource(Register, '/auth/register')
API.add_resource(Login, '/auth/login')
