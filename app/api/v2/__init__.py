from flask import Blueprint
from flask_restful import Api
from .views.incidences_views import RedFlags, RedFlagsSpecific

version_two = Blueprint("v2", __name__, url_prefix="/api/v2")
API = Api(version_two)


API.add_resource(RedFlags, '/incidences')
API.add_resource(RedFlagsSpecific, '/incidences/<int:id>')

