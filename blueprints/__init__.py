from sanic import Blueprint
from .api import api

bp = Blueprint.group(api, url_prefix='/api')
