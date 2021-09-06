from sanic import Blueprint
from .blueprints import api
from . import models

tortoise_demo_api = Blueprint.group(api, url_prefix='/tortoise/demo')