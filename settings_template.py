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


class RPC:
    _start = True


class Auth:
    _start = True
    secret = ''
    expiration_delta = 60 * 60 * 24


class SMS:
    key = ''
    secret = ''
    sign_name = ''
    template_code = ''


class PrueSQL:
    _start = True

    class AsyncPG(Settings):
        _start = True

        # asyncpg 中的连接参数
        host = '192.168.1.63'
        port = '5432'
        user = ''
        password = ''
        database = ''
        min_size = 5
        max_size = 20


class ORM:
    _start = True

    class SQLAlchemy:
        _start = True

        db_host = 'localhost'
        db_port = '5432'
        db_name = 'tailor'
        db_user = ''
        db_pass = ''

    class TortoiseORM(Settings):
        _start = True

        connections = {
                # Dict format for connection
                'default': {
                    'engine': 'tortoise.backends.asyncpg',
                    'credentials': {
                        'host': '',
                        'port': 5432,
                        'user': '',
                        'password': '',
                        'database': ''
                    }
                },
            }

        apps = {
                'models': {
                    'models': ['addons.tortoise_demo.__models__', 'aerich.models'],  # todo: add models
                    # If no default_connection specified, defaults to 'default'
                    'default_connection': 'default',
                }
            }

        use_tz = True


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


TORTOISE_ORM = ORM.TortoiseORM.get_values()