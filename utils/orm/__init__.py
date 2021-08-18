#! -*- coding: utf-8 -*-
from settings import ORM


def init_orm(app):

    if ORM.TortoiseORM._start:
        from . import tortoise_orm

        tortoise_config = dict(ORM.TortoiseORM())
        tortoise_orm.init_orm(app, tortoise_config)
