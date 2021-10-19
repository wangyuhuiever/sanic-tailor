#! -*- coding: utf-8 -*-
import asyncpg
import asyncio
import inspect
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

    id = None
    ids = None

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

    async def search(self, condition, fields='*'):
        where_list = []
        values = []
        for k, v in condition.items():
            values.append(v)
            where_list.append(f'{k}=${len(values)}')
        where_str = ' and '.join(where_list)
        sql = f"select {fields} from {self._table} where {where_str};"
        res = await self.execute(sql, values)
        for r in res:
            self.id = r.get('id')
        return self



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
