# -*- coding: utf-8 -*-
import settings
from . import db
from . import celery


def init_utils(app):

    if settings.Database.start:
        app.update_config(settings.Database)

        @app.listener('before_server_start')
        async def init_database(app, loop):
            await db.init_database(app, loop)

        @app.listener('after_server_stop')
        async def close_database(app, loop):
            await db.close_database(app, loop)

    if settings.Celery.start:
        app.update_config(settings.Celery)

        @app.listener('main_process_start')
        async def init_celery(app, loop):
            await celery.init_celery(app, loop)

        @app.listener('main_process_stop')
        async def close_celery(app, loop):
            await celery.close_celery(app, loop)
