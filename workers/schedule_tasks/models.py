from workers import app
from workers.utils.db import Database
# import asyncio
import logging

_logger = logging.getLogger(__name__)
database = Database(
    app.conf.custom_db_host,
    app.conf.custom_db_port,
    app.conf.custom_db_user,
    app.conf.custom_db_pass,
    app.conf.custom_db_name,
)


def insert_db():
    sql = "insert into test_table (col1, col2) values (%s, %s) returning id;"
    values = [1, 'test']
    res = database.insert(sql, tuple(values))
    _logger.info({'insert_res': res})
    data = [dict(r) for r in res]
    _logger.info({'insert_db': data})
    return data


def select_db(res_id):
    sql = "select * from test_table where id = %s;"
    values = [res_id]
    res = database.query(sql, tuple(values))
    _logger.info({'select_res': res})
    data = [dict(r) for r in res]
    _logger.info({'select_db': data})
    return data


@app.task(name='schedule_task')
def schedule_task(*args, **kwargs):
    _logger.info({
        'args': args,
        'kwargs': kwargs
    })
    rec_id = insert_db()
    _logger.info({'schedule_task id': rec_id})
    res_id = rec_id[0].get('id')
    res = select_db(res_id)
    _logger.info({'schedule_task res': res})
    return


@app.task(name='cron_task')
def cron_task(*args, **kwargs):
    _logger.info({
        'args': args,
        'kwargs': kwargs
    })
    return
