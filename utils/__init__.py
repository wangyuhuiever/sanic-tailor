# -*- coding: utf-8 -*-
import settings
from . import db
from . import celery
from . import redis


def init_utils(app):

    if settings.Database.start:
        @app.listener('before_server_start')
        async def init_database(app, loop):
            await db.init_database(app, loop)

        @app.listener('after_server_stop')
        async def close_database(app, loop):
            await db.close_database(app, loop)

    if settings.Celery.start:
        @app.listener('main_process_start')
        async def init_celery(app, loop):
            await celery.init_celery(app, loop)

        @app.listener('main_process_stop')
        async def close_celery(app, loop):
            await celery.close_celery(app, loop)

    if settings.Redis.start:
        @app.listener('after_server_start')
        async def init_redis(app, loop):
            await redis.init_redis(app, loop)

        @app.listener('after_server_stop')
        async def close_redis(app, loop):
            await redis.close_redis(app, loop)

