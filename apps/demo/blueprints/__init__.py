# -*- coding: utf-8 -*-
from sanic import Blueprint

from .models import api

demo_api = Blueprint.group(api, url_prefix='/demo')