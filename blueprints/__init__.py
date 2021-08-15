from sanic import Blueprint
from .demo import demo

bp = Blueprint.group(demo, url_prefix='/api')


from .demo.models import *