#! -*- coding: utf-8 -*-
from settings import PrueSQL
from . import asyncpg as psql


def init_pure_sql(app):

    if 'AsyncPG' in dir(PrueSQL) and PrueSQL.AsyncPG._start:
        @app.listener('before_server_start')
        async def init_database(app, loop):
            await psql.init_database(app, loop)

        @app.listener('after_server_stop')
        async def close_database(app, loop):
            await psql.close_database(app, loop)