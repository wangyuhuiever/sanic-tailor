#! -*- coding: utf-8 -*-
import json
import copy
import asyncpg
import asyncio
import inspect
import datetime
from sanic import exceptions
from settings import PrueSQL
from sanic.log import logger as _logger


MODEL_RECORDS = []
FUNCTION_RECORDS = []


class Models:
    name = None
    model = None

    def __init__(self, name:str, model:object, **kwargs):
        self.name = name
        self.model = model
        self.__dict__.update(kwargs)

    @classmethod
    def get(cls, name):
        models = list(filter(lambda m: m.name == name, MODEL_RECORDS))
        return models[0] if models else cls

    def get_function(self, name):
        functions = list(filter(lambda r: r.model == self.model and r.name == name, FUNCTION_RECORDS))
        return functions[0] if functions else None


class Functions:
    name = None
    model = None
    function = None

    def __init__(self, name:str, model:Models, function, **kwargs):
        self.name = name
        self.model = model
        self.function = function
        self.__dict__.update(kwargs)


class Database(object):

    _name = None
    _inherit = None
    _abstract = None
    _table = None

    _fields = ['id', 'ids']

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if not k.startswith('_') and k in self._fields:
                self.__setattr__(k, v)

    def __new__(cls, *args, **kwargs):
        instance = super(Database, cls).__new__(cls)
        for k in instance._fields:
            if k not in kwargs:
                instance.__setattr__(k, None)
        return instance

    @classmethod
    async def init(cls, pool):
        cls.pool = pool

    @classmethod
    async def close(cls):
        await asyncio.wait_for(cls.pool.close(), 10)
        cls.pool = {}

    async def execute(self, sql, *args):
        async with self.pool.acquire() as connection:
            value = await connection.fetch(sql, *args)
        return value

    async def update(self, data):
        for k, v in data.items():
            self.__setattr__(k, v)

    async def copy(self):
        nself = Models.get(self._name).model()
        values = {}
        for f in self._fields:
            values.update({f: self.__getattribute__(f)})
        await nself.update(values)
        return nself

    async def read(self, fields=None):
        if not fields:
            fields = self._fields
        else:
            if any(f not in self._fields for f in fields):
                raise exceptions.abort(200, "can not read all fields!")

        res = {k: self.__getattribute__(k) for k in fields}
        return res

    async def search(self, condition, fields='*'):
        if isinstance(fields, list):
            fields = ','.join(fields)
        where_list = []
        values = []
        for k, v in condition.items():
            values.append(v)
            where_list.append(f'{k}=${len(values)}')
        where_str = ' and '.join(where_list)
        sql = f"select {fields} from {self._table} where {where_str};"
        res = await self.execute(sql, *values)
        record_list = []
        for r in res:
            nself = await self.copy()
            await nself.update(r)
            record_list.append(nself)
        return record_list

    async def create_single(self, data):
        if not data:
            raise exceptions.abort(403, '创建出错，无数据！')
        if not isinstance(data, dict):
            raise Warning('Field values must be dictionary type.')

        data.update({
            'create_uid': 1,
            'create_date': datetime.datetime.utcnow(),
            'write_uid': 1,
            'write_date': datetime.datetime.utcnow()
        })

        field_list = ','.join(data.keys())
        value_list = tuple(data.values())
        value_string_list = list(map(lambda k: '$' + str(k), range(1, len(value_list) + 1)))
        value_string = ','.join(value_string_list)
        insert_sql = f"INSERT INTO {self._table} ({field_list}) VALUES (" + value_string + ") RETURNING id;"
        ids = await self.execute(insert_sql, *value_list)
        return ids[0]['id']

    async def update_single(self, condition, data):
        if not isinstance(condition, dict):
            raise Warning('Field condition must be dictionary type.')
        if not isinstance(data, dict):
            raise Warning('Field data must be dictionary type.')
        data.update({
            'write_uid': 1,
            'write_date': datetime.datetime.utcnow()
        })
        update_str_list = []
        where_str_list = []
        values = []
        for k, v in data.items():
            values.append(v)
            update_str_list.append(f'{k}=${len(values)}')

        for k, v in condition.items():
            values.append(v)
            where_str_list.append(f'{k}=${len(values)}')

        update_str = ','.join(update_str_list)
        where_str = ','.join(where_str_list)

        update_sql = f"UPDATE {self._table} SET {update_str} WHERE {where_str} RETURNING id;"
        update_ids = await self.execute(update_sql, *values)
        return update_ids[0]['id']


def get_all_classes(base_model):
    """
    获取父类的所有子类
    """
    all_classes = {}
    all_functions = {}
    for subclass in base_model.__subclasses__():
        # 所有抽象类不注册
        if not subclass._abstract:
            # 1. 如果类名已经注册，则需要注册更基础的子类，同时增加子类的__bases__
            # 2. 如果类名尚未注册，则直接注册
            subclass_name = subclass._name or subclass._inherit
            if not subclass._table and subclass._name:
                subclass._table = subclass._name.replace('.', '_')
            if subclass_name in all_classes.keys():
                old_class = all_classes[subclass_name]
                bases = old_class.__bases__
                new_bases = list(bases)
                if old_class not in new_bases:
                    new_bases.insert(0, old_class)
                subclass.__bases__ = tuple(new_bases)

            functions = inspect.getmembers(subclass, predicate=inspect.isfunction)

            all_classes[subclass_name] = subclass
            all_functions[subclass_name] = functions


        get_all_classes(subclass)
    return all_classes, all_functions

def _set_up_models(base_model):
    classes, functions = get_all_classes(base_model)
    for k, v in classes.items():
        MODEL_RECORDS.append(Models(name=k, model=v))

    for k, v in functions.items():
        model = classes.get(k)
        for func in v:
            FUNCTION_RECORDS.append(Functions(name=func[0], model=model, function=func[1]))


async def init_database(app, loop):
    _logger.info("Database starting...")
    config = PrueSQL.AsyncPG.get_values()
    _logger.debug({'database setting': config})
    pool = await asyncpg.create_pool(
        **config
    )
    await Database.init(pool)
    _set_up_models(Database)


async def close_database(app, loop):
    _logger.info("Database stopping...")
    await Database.close()
