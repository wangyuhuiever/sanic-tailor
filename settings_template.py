# -*- coding: utf-8 -*-

class Settings:
    """
    获取字典
    """

    @classmethod
    def get_values(cls):
        d = dict(vars(cls))
        private = [i for i in d.keys() if i.startswith('_')]
        for k in private:
            d.pop(k)
        return d


class Sanic:
    name = "Sanic Tailor"

    SANIC_JWT_SECRET = "hard to guess"
    SANIC_JWT_EXPIRATION_DELTA = 60 * 60 * 24


class RPC:
    _start = True


class SMS:
    key = ''
    secret = ''
    sign_name = ''
    template_code = ''


class ORM:
    _start = True

    class SQLAlchemy:
        _start = True

        db_host = 'localhost'
        db_port = '5432'
        db_name = 'tailor'
        db_user = ''
        db_pass = ''


class RabbitMQ:
    HOST = '192.168.1.63'
    PORT = '5672'
    API_PORT = '15672'
    USER = ''
    PASS = ''
    VHOST = ''


class Redis:
    _start = True

    HOST = '192.168.1.63'
    PORT = '6379'
    PASS = ''
    DB = '8'
    PREFIX = 'sanic:cache'


class Celery:
    name = "Sanic Tailor Celery"
    _start = True

    custom_db_host = ORM.SQLAlchemy.db_host
    custom_db_port = ORM.SQLAlchemy.db_port
    custom_db_user = ORM.SQLAlchemy.db_user
    custom_db_pass = ORM.SQLAlchemy.db_pass
    custom_db_name = ORM.SQLAlchemy.db_name

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
