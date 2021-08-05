# -*- coding: utf-8 -*-

class Sanic:
    name = "Yuhui Sanic"

    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_USER = ''
    DB_PASS = ''
    DB_NAME = ''

    MQ_HOST = ''
    MQ_PORT = ''
    MQ_USER = ''
    MQ_PASS = ''
    MQ_VHOST = ''

    REDIS_HOST = ''
    REDIS_PORT = ''
    REDIS_PASS = ''
    REDIS_DB = ''


class Celery:
    name = "Yuhui Sanic Celery"

    custom_db_host = Sanic.DB_HOST
    custom_db_port = Sanic.DB_PORT
    custom_db_user = Sanic.DB_USER
    custom_db_pass = Sanic.DB_PASS
    custom_db_name = Sanic.DB_NAME

    custom_flower_port = ''
    custom_flower_user = ''
    custom_flower_pass = ''

    broker_url = f'amqp://{Sanic.MQ_USER}:{Sanic.MQ_PASS}@{Sanic.MQ_HOST}:{Sanic.MQ_PORT}/{Sanic.MQ_VHOST}'
    result_backend = f'redis://default:{Sanic.REDIS_PASS}@{Sanic.REDIS_HOST}:{Sanic.REDIS_PORT}/{Sanic.REDIS_DB}'
    result_expires = 3600
    enable_utc = True
    beat_schedule = {
        'schedule_task': {
            'task': 'schedule_task',
            'schedule': 60,  # 默认一分钟
            'args': (1, 2),
            'kwargs': {'a': 'a'}
        }
    }

