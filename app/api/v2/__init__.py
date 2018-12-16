from flask import Blueprint
from flask_restful import Api
from .views.users_views import Login, Register
from .views.incidences_views import Incidences, Incidence, IncidentLocation, IncidentComment, IncidentStatus

version_two = Blueprint("v2", __name__, url_prefix="/api/v2")
API = Api(version_two)


API.add_resource(Login, '/auth/login/')
API.add_resource(Register, '/auth/register/')
API.add_resource(Incidences, '/incidences/')
API.add_resource(Incidence, '/incidences/<int:incident_id>/')
API.add_resource(IncidentLocation, '/incidences/<int:incident_id>/location')
API.add_resource(IncidentComment, '/incidences/<int:incident_id>/comment')
API.add_resource(IncidentStatus, '/incidences/<int:incident_id>/status')

 
