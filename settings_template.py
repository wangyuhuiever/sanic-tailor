# -*- coding: utf-8 -*-

class Sanic:
    name = "Yuhui Sanic"


class Database:
    start = True

    HOST = 'localhost'
    PORT = '5432'
    USER = ''
    PASS = ''
    NAME = ''


class RabbitMQ:
    HOST = ''
    PORT = ''
    USER = ''
    PASS = ''
    VHOST = ''


class Redis:
    start = True

    HOST = ''
    PORT = ''
    PASS = ''
    DB = ''


class Celery:
    name = "Yuhui Sanic Celery"
    start = True

    custom_db_host = Database.HOST
    custom_db_port = Database.PORT
    custom_db_user = Database.USER
    custom_db_pass = Database.PASS
    custom_db_name = Database.NAME

    custom_flower_port = ''
    custom_flower_user = ''
    custom_flower_pass = ''
    custom_loglevel = 'info'

    broker_url = f'amqp://{RabbitMQ.USER}:{RabbitMQ.PASS}@{RabbitMQ.HOST}:{RabbitMQ.PORT}/{RabbitMQ.VHOST}'
    result_backend = f'redis://default:{Redis.PASS}@{Redis.HOST}:{Redis.PORT}/{Redis.DB}'
    result_expires = 3600
    beat_schedule_filename = '/tmp/celerybeat-schedule'
    enable_utc = True
    beat_schedule = {
        'schedule_task': {
            'task': 'schedule_task',
            'schedule': 60,  # 默认一分钟
            'args': (1, 2),
            'kwargs': {'a': 'a'}
        }
    }

