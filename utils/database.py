import settings
import asyncpg
# from async_lru import alru_cache


class Database(object):

    def __init__(self):
        self.db_user = settings.DB_USER
        self.db_pass = settings.DB_PASS
        self.db_name = settings.DB_NAME
        self.db_host = settings.DB_HOST
        self.db_port = settings.DB_PORT

    async def execute(self, sql, *args):
        conn = await asyncpg.connect(user=self.db_user, password=self.db_pass, database=self.db_name, host=self.db_host,
                                     port=self.db_port)
        values = await conn.fetch(sql, *args)
        await conn.close()
        return values


def mount_database(app, loop):
    app.database = Database()


