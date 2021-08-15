#! -*- coding: utf-8 -*-
from settings import ORM
from . import tortoise_orm


def init_orm(app):

    if ORM.TortoiseORM._start:
        tortoise_config = dict(ORM.TortoiseORM())
        tortoise_orm.init_orm(app, tortoise_config)
