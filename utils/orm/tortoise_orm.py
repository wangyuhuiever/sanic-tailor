#! -*- coding: utf-8 -*-
from sanic.log import logger as _logger
from tortoise.contrib.sanic import register_tortoise
from tortoise.models import Model
from tortoise import fields
import inspect

def init_tortoise(app, config):
    _logger.info("Tortoise ORM starting...")
    global __models__
    __models__ += list(map(lambda r: r.model, MODEL_RECORDS))
    register_tortoise(
        app,
        config=config,
        generate_schemas=True
    )


class BaseUser(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)


    class Meta:
        # table = 'base_users'
        name = 'app.users'
        ordering = ["id"]

    def __str__(self):
        return self.name


class BaseModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    create_uid = fields.ForeignKeyField('models.BaseUser', related_name='cu', null=True, on_delete=fields.SET_NULL)
    create_date = fields.DatetimeField(auto_now_add=True)
    write_uid = fields.ForeignKeyField('models.BaseUser', related_name='wu', null=True, on_delete=fields.SET_NULL)
    write_date = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-id"]

    def __str__(self):
        return self.name or False


MODEL_RECORDS = []
FUNCTION_RECORDS = []

__models__ = [BaseUser, BaseModel]


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


def get_all_classes(base_model):
    """
    获取父类的所有子类
    """
    all_classes = {}
    all_functions = {}
    for subclass in base_model.__subclasses__():
        # 所有抽象类不注册
        if not getattr(subclass.Meta, 'abstract', None):
            # 1. 如果类名已经注册，则需要注册更基础的子类，同时增加子类的__bases__
            # 2. 如果类名尚未注册，则直接注册
            subclass_name = getattr(subclass.Meta, 'name', None) or subclass.Meta.inherit
            if not getattr(subclass.Meta, 'table', None) and getattr(subclass.Meta, 'name', None):
                setattr(subclass.Meta, 'table', subclass.Meta.name.replace('.', '_'))
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


_set_up_models(BaseModel)
_set_up_models(BaseUser)
