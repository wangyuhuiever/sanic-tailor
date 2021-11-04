from sanic import Blueprint
from .demo import demo_api


api = Blueprint.group(
    demo_api,
    url_prefix='/api'
)
