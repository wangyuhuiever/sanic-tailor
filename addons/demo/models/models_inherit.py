from utils.pure_sql.asyncpg import Database


class DemoModel(Database):
    _inherit = "demo.model"

    async def demo_method(self):
        print('demo inherit')