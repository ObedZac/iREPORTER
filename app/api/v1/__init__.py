from flask import Blueprint
from flask_restful import Api
from .views.incidences_views import RedFlags, RedFlagsSpecific

version_one = Blueprint("v1", __name__, url_prefix="/api/v1")
API = Api(version_one)


API.add_resource(RedFlags, '/redflags')
API.add_resource(RedFlagsSpecific, '/redflags/<int:id>')
