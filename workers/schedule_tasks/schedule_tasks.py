from workers import app
from workers.utils.database import database
import asyncio
import logging

_logger = logging.getLogger(__name__)


async def insert_db():
    sql = "insert into test_table (col1, col2) values ($1, $2) returning id;"
    values = [1, 'test']
    res = await database.execute(sql, *values)
    print(res)
    return


@app.task(name='schedule_task')
def schedule_task(*args, **kwargs):
    _logger.info({
        'args': args,
        'kwargs': kwargs
    })
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert_db())
    return



