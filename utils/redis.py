import aioredis
import settings
from sanic.log import logger as _logger
from async_lru import alru_cache


class Redis(object):
    prefix = settings.Redis.PREFIX + ":"

    @classmethod
    async def init(cls, pool):
        cls.pool = pool
        cls.redis = aioredis.Redis(connection_pool=pool)

    @classmethod
    async def close(cls):
        await cls.pool.disconnect()

    async def set(self, name, value, ex=None, px=None, nx=False, xx=False, keepttl=False):
        name = self.prefix + name
        res = await self.redis.set(name, value, ex, px, nx, xx, keepttl)
        return res

    async def ttl(self, name):
        name = self.prefix + name
        res = await self.redis.ttl(name)
        return res

    async def get(self, name):
        name = self.prefix + name
        value = await self.redis.get(name)
        return value

    async def execute_command(self, *args, **options):
        value = await self.redis.execute_command(*args, **options)
        return value


async def init_redis(app, loop):
    _logger.info("Redis starting...")
    pool = aioredis.ConnectionPool(
        host=settings.Redis.HOST,
        port=settings.Redis.PORT,
        db=settings.Redis.DB,
        password=settings.Redis.PASS,
        encoding='utf-8',
        decode_responses=True
    )
    await Redis.init(pool)
    app.cache = await Redis().redis


async def close_redis(app, loop):
    _logger.info("Redis stopping...")
    app.cache = None
    await Redis.close()
