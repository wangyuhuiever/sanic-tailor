from utils.pure_sql.asyncpg import Database
from utils.redis import Redis
import httpx
import json
import logging

_logger = logging.getLogger(__name__)


class DemoModel(Database, Redis):

    async def cache_data(self, id, data):
        value = json.dumps(data)
        key = f'test_model:{id}'
        set_res = await self.set(key, value)
        _logger.info({'set res': set_res})
        get_res = await self.get(key)
        _logger.info({'get res': get_res})
        get_res = json.loads(get_res)
        return get_res

    async def insert_data(self):
        async with httpx.AsyncClient() as client:
            headers = {}
            payload = {}
            response = await client.get("http://www.baidu.com", headers=headers)

        result = response.text
        sql = "insert into test_table (col1, col2) values ($1, $2) returning id;"
        values = [1, result]
        insert_res = await self.execute(sql, *values)
        query_sql = "select * from test_table where id=$1;"
        query_res = await self.execute(query_sql, insert_res[0].get('id'))
        query_dict = [dict(q) for q in query_res]
        redis_res = await self.cache_data(query_dict[0].get('id'), query_dict[0])
        return redis_res
