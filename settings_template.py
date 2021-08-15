# -*- coding: utf-8 -*-

class Settings:
    """
    通过dict获取到字典
    """
    def __iter__(self):
        for k in dir(self):
            if k and not k.startswith('_'):
                v = getattr(self, k)
                yield (k, v)
            else:
                continue


class Sanic:
    name = "Sanic Tailor"


class PrueSQL:
    _start = True

    class AsyncPG(Settings):
        _start = True

        # asyncpg 中的连接参数
        host = '192.168.1.63'
        port = '5432'
        user = 'yuhui'
        password = 'yuhui.123'
        database = 'yudb'
        min_size = 5
        max_size = 20


class RabbitMQ:
    HOST = '192.168.1.63'
    PORT = '5672'
    API_PORT = '15672'
    USER = 'yuhui'
    PASS = '6MsziVeSetJW0ies'
    VHOST = 'yuhui'


class Redis:
    _start = True

    HOST = '192.168.1.63'
    PORT = '6379'
    PASS = 'OrWc8SJ71j8O4nfu'
    DB = '8'
    PREFIX = 'sanic:cache'


class Celery:
    name = "Sanic Tailor Celery"
    _start = True

    custom_db_host = PrueSQL.AsyncPG.host
    custom_db_port = PrueSQL.AsyncPG.port
    custom_db_user = PrueSQL.AsyncPG.user
    custom_db_pass = PrueSQL.AsyncPG.password
    custom_db_name = PrueSQL.AsyncPG.database

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

