from utils.db import Database
import httpx


class DemoModel(Database):

    async def insert_data(self):
        async with httpx.AsyncClient() as client:
            headers = {}
            payload = {}
            response = await client.get("http://www.baidu.com", headers=headers)

        r = response.text
        sql = "insert into test_table (col1, col2) values ($1, $2) returning id;"
        values = [1, r]
        res = await self.execute(sql, *values)
        return res