#! -*- coding: utf-8 -*-
from settings import ORM


def init_orm(app):

    if 'SQLAlchemy' in dir(ORM) and ORM.SQLAlchemy._start:
        from . import _sqlalchemy

        _sqlalchemy.init_sqlalchemy(app, ORM.SQLAlchemy)
    #
    # if 'TortoiseORM' in dir(ORM) and ORM.TortoiseORM._start:
    #     from . import tortoise_orm
    #
    #     tortoise_orm.init_tortoise(app, ORM.TortoiseORM.TORTOISE_ORM)
    #
    # if 'GINO' in dir(ORM) and ORM.GINO._start:
    #     from . import gino_orm
    #
    #     gino_orm.init_gino(app, ORM.GINO)
