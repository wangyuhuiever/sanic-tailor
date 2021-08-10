from workers import app
from workers.utils.db import database
from celery.schedules import crontab
import asyncio
import logging

_logger = logging.getLogger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    # 每10秒触发一次
    sender.add_periodic_task(10, schedule_task.s('args: ', '1', '2', kwarg='kwarg', kwarg2='kwarg2'))

    # 每天10点30触发一次
    sender.add_periodic_task(
        crontab(hour=10, minute=30),
        cron_task.s('cron args:', '1', '2', kwarg='kwarg')
    )


async def insert_db():
    sql = "insert into test_table (col1, col2) values ($1, $2) returning id;"
    values = [1, 'test']
    res = await database.execute(sql, *values)
    data = [dict(r) for r in res]
    _logger.info({'insert_db': data})
    return data


async def select_db(res_id):
    sql = "select * from test_table where id = $1;"
    values = [res_id]
    res = await database.execute(sql, *values)
    data = [dict(r) for r in res]
    _logger.info({'select_db': data})
    return data


@app.task(name='schedule_task')
def schedule_task(*args, **kwargs):
    _logger.info({
        'args': args,
        'kwargs': kwargs
    })
    loop = asyncio.get_event_loop()
    res_id = loop.run_until_complete(insert_db())
    _logger.info({'schedule_task id': res_id})
    res_id = res_id[0].get('id')
    res = loop.run_until_complete(select_db(res_id))
    _logger.info({'schedule_task res': res})
    return


@app.task(name='cron_task')
def cron_task(*args, **kwargs):
    _logger.info({
        'args': args,
        'kwargs': kwargs
    })
    return
