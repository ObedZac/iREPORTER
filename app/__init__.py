"""App blueprints configuration"""
from flask import Flask, Blueprint
from .api.v1 import version_one as v1
from .api.v2 import version_two as v2
from instance.config import app_config


def create_app(config_name):
    """Defining the blueprint"""
    APP = Flask(__name__, instance_relative_config=True)
    APP.url_map.strict_slashes = False
    APP.config.from_object(app_config[config_name])
    APP.config.from_pyfile('config.py')


    APP.register_blueprint(v1)

    # APP.register_blueprint(v2)

    return APP
