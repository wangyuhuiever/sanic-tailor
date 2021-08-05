# -*- coding: utf-8 -*-
import settings
from celery import Celery

app = Celery(settings.Celery.name)

app.config_from_object(settings.Celery)

from . import tasks
from . import schedule_tasks
