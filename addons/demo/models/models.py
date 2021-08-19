from utils.pure_sql.asyncpg import Database
from utils.redis import Redis
import httpx
import json
from sanic.log import logger as _logger


class DemoModel(Database, Redis):

    async def cache_data(self, id, data):
        value = json.dumps(data)
        key = f'test_model:{id}'
        set_result = await self.set(key, value)
        _logger.info({'set_result': set_result})
        get_record = await self.get(key)
        _logger.info({'get_record': get_record})
        get_record = json.loads(get_record)
        return get_record

    async def insert_data(self):
        async with httpx.AsyncClient() as client:
            headers = {}
            payload = {}
            response = await client.get("http://www.baidu.com", headers=headers)

        result = response.text
        sql = "insert into test_table (col1, col2) values ($1, $2) returning id;"
        values = [1, result]
        insert_result = await self.execute(sql, *values)
        query_sql = "select * from test_table where id=$1;"
        query_records = await self.execute(query_sql, insert_result[0].get('id'))
        query_dict = [dict(q) for q in query_records]
        redis_result = await self.cache_data(query_dict[0].get('id'), query_dict[0])
        return redis_result
