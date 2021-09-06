#! -*- coding: utf-8 -*-
import asyncpg
import asyncio
from settings import PrueSQL
from sanic.log import logger as _logger
import socket


class Database(object):

    @classmethod
    async def init(cls, pool):
        cls.pool = pool

    @classmethod
    async def close(cls):
        await asyncio.wait_for(cls.pool.close(), 10)
        cls.pool = {}

    async def execute(self, sql, *args):
        async with self.pool.acquire() as connection:
            value = await connection.fetch(sql, *args)
        return value


async def init_database(app, loop):
    _logger.info("Database starting...")
    config = dict(PrueSQL.AsyncPG())
    _logger.debug({'database setting': config})
    pool = await asyncpg.create_pool(
        **config
    )
    await Database.init(pool)


async def close_database(app, loop):
    _logger.info("Database stopping...")
    await Database.close()


# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(("localhost", 5000))
# sock.listen(1)
# while True:
#     conn, addr = sock.accept()
#     print(conn.recv(1024))
#     conn.sendall()