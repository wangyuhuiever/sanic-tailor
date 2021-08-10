import asyncpg
import settings
from sanic.log import logger as _logger


class Database(object):

    @classmethod
    async def init(cls, pool):
        cls.pool = pool

    @classmethod
    async def close(cls):
        cls.pool = {}

    async def execute(self, sql, *args):
        async with self.pool.acquire() as connection:
            value = await connection.fetch(sql, *args)
            return value


async def init_database(app, loop):
    _logger.info("Database starting...")
    pool = await asyncpg.create_pool(
        host=settings.Database.HOST,
        port=settings.Database.PORT,
        user=settings.Database.USER,
        password=settings.Database.PASS,
        database=settings.Database.NAME,
        min_size=5,
        max_size=20
    )
    await Database.init(pool)


async def close_database(app, loop):
    _logger.info("Database stopping...")
    await Database.close()


class AnotherDatabase(object):
    def __init__(self, db_host, db_port, db_user, db_pass, db_name):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    async def execute(self, sql, *args):
        conn = await asyncpg.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            database=self.db_name,
        )
        values = await conn.fetch(sql, *args)
        await conn.close()
        return values
