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
    PORT = '5672'
    API_PORT = '15672'
    USER = ''
    PASS = ''
    VHOST = ''


class Redis:
    start = True

    HOST = ''
    PORT = '6379'
    PASS = ''
    DB = '8'
    PREFIX = 'sanic:cache'


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
    task_default_queue = "5f77d2fe-c30b-4b30-b370-79141ceecad8"  # 重要，同一个broker用来隔离数据，建议使用uuid
    redis_max_connections = 100
    result_expires = 3600
    beat_schedule_filename = '/tmp/celerybeat-schedule'
    timezone = 'Asia/Shanghai'
    # enable_utc = True


