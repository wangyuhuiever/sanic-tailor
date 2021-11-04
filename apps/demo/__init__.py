from sanic import Blueprint
from .blueprints import api
from . import models

demo_api = Blueprint.group(api, url_prefix='/demo')