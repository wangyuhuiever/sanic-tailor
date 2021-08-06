# -*- coding: utf-8 -*-

class Sanic:
    name = "Yuhui Sanic"


class Database:
    start = True

    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_USER = ''
    DB_PASS = ''
    DB_NAME = ''


class RabbitMQ:
    MQ_HOST = ''
    MQ_PORT = '5672'
    MQ_API_PORT = '15672'
    MQ_USER = ''
    MQ_PASS = ''
    MQ_VHOST = ''


class Redis:
    REDIS_HOST = ''
    REDIS_PORT = '6379'
    REDIS_PASS = ''
    REDIS_DB = '8'


class Celery:
    name = "Yuhui Sanic Celery"
    start = True

    custom_db_host = Database.DB_HOST
    custom_db_port = Database.DB_PORT
    custom_db_user = Database.DB_USER
    custom_db_pass = Database.DB_PASS
    custom_db_name = Database.DB_NAME

    custom_flower_port = ''
    custom_flower_user = ''
    custom_flower_pass = ''
    custom_loglevel = 'info'

    broker_url = f'amqp://{RabbitMQ.MQ_USER}:{RabbitMQ.MQ_PASS}@{RabbitMQ.MQ_HOST}:{RabbitMQ.MQ_PORT}/{RabbitMQ.MQ_VHOST}'
    result_backend = f'redis://default:{Redis.REDIS_PASS}@{Redis.REDIS_HOST}:{Redis.REDIS_PORT}/{Redis.REDIS_DB}'
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

