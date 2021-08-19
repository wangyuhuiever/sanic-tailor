from sanic import Blueprint
from .demo import demo_api
from .demo.models import *


api = Blueprint.group(
    demo_api,
    url_prefix='/api'
)

