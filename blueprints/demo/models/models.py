from utils.db import Database


class DemoModel(Database):

    async def insert_data(self):
        sql = "insert into test_table (col1, col2) values ($1, $2) returning id;"
        values = [1, 'test']
        res = await self.execute(sql, *values)
        return res