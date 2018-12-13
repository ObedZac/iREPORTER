"""App blueprints configuration"""
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from .api.v1 import version_one as v1
from .api.v2 import version_two as v2
from instance.config import app_config

jwt = JWTManager()

def create_app(config_name):
    """Defining the blueprint"""
    APP = Flask(__name__, instance_relative_config=True)
    APP.url_map.strict_slashes = False
    APP.config.from_object(app_config[config_name])
    APP.config.from_pyfile('config.py')
    
    jwt.init_app(APP)
    APP.config['JWT_SECRET_KEY'] = 'week2'


    # APP.register_blueprint(v1)

    APP.register_blueprint(v2)

    return APP
