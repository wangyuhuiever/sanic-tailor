import asyncpg
# from async_lru import alru_cache


class Database(object):

    def __init__(self, pool=None):
        self.pool = pool

    async def execute(self, sql, *args):
        async with self.pool.acquire() as connection:
            value = await connection.fetch(sql, *args)
            return value

    async def close(self):
        await self.pool.close()


async def init_database(app, loop):
    pool = await asyncpg.create_pool(
        host=app.config.DB_HOST,
        port=app.config.DB_PORT,
        user=app.config.DB_USER,
        password=app.config.DB_PASS,
        database=app.config.DB_NAME,
        min_size=5,
        max_size=100
    )

    app.database = Database(pool=pool)


async def close_database(app, loop):
    await app.database.close()


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
