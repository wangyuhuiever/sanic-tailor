from sanic import Blueprint
from .blueprints import api

demo_api = Blueprint.group(api, url_prefix='/demo')