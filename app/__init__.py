from flask import Flask, Blueprint
from .api.v1 import version_one as v1
from instance.config import app_config
# from .db_config import create_tables


def create_app(config_name='development'):
    APP = Flask(__name__, instance_relative_config = True)
    APP.url_map.strict_slashes = False
    APP.config.from_object(app_config[config_name])
    APP.config.from_pyfile('config.py')

    # create-tables()

    APP.register_blueprint(v1)

    return APP


APP = create_app()


# def create_app():
#     APP= Flask(__name__)
#     APP.register_blueprint(v1)
#     return APP
