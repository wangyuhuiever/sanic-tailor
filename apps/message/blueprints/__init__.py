# -*- coding: utf-8 -*-
from sanic import Blueprint

from .models import api

message_api = Blueprint.group(api, url_prefix='/message')