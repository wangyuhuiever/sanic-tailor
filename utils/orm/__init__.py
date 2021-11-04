#! -*- coding: utf-8 -*-
from settings import ORM


def init_orm(app):

    if 'SQLAlchemy' in dir(ORM) and ORM.SQLAlchemy._start:
        from . import _sqlalchemy

        _sqlalchemy.init_sqlalchemy(app, ORM.SQLAlchemy)
