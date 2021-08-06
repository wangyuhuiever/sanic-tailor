from sanic import Blueprint
from .apis import api

demo = Blueprint.group(api, url_prefix='/demo')
