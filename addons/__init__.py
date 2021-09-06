from sanic import Blueprint
from .demo import demo_api
from .tortoise_demo import tortoise_demo_api


api = Blueprint.group(
    demo_api,
    tortoise_demo_api,
    url_prefix='/api'
)

