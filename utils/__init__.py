# -*- coding: utf-8 -*-
import settings
from . import pure_sql
from . import celery
from . import redis
from . import orm
from . import auth


def init_utils(app):

    if settings.PrueSQL._start:
        pure_sql.init_pure_sql(app)

    if settings.Auth._start:
        auth.init_auth(app)

    if settings.ORM._start:
        orm.init_orm(app)

    if settings.Celery._start:
        @app.listener('main_process_start')
        async def init_celery(app, loop):
            await celery.init_celery(app, loop)

        @app.listener('main_process_stop')
        async def close_celery(app, loop):
            await celery.close_celery(app, loop)

    if settings.Redis._start:
        @app.listener('after_server_start')
        async def init_redis(app, loop):
            await redis.init_redis(app, loop)

        @app.listener('after_server_stop')
        async def close_redis(app, loop):
            await redis.close_redis(app, loop)

