# -*- coding: utf-8 -*-
import settings
from . import celery
from . import redis
from . import auth
from . import rpc
from . import orm


def init_utils(app):

    if 'RPC' in dir(settings) and settings.RPC._start:
        rpc.init_rpc(app)

    if 'Auth' in dir(settings) and settings.Auth._start:
        auth.init_auth(app)

    if 'ORM' in dir(settings) and settings.ORM._start:
        orm.init_orm(app)

    if 'Celery' in dir(settings) and settings.Celery._start:
        @app.listener('main_process_start')
        async def init_celery(app, loop):
            await celery.init_celery(app, loop)

        @app.listener('main_process_stop')
        async def close_celery(app, loop):
            await celery.close_celery(app, loop)

    if 'Redis' in dir(settings) and settings.Redis._start:
        @app.listener('after_server_start')
        async def init_redis(app, loop):
            await redis.init_redis(app, loop)

        @app.listener('after_server_stop')
        async def close_redis(app, loop):
            await redis.close_redis(app, loop)

