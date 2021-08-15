#! -*- coding: utf-8 -*-
from tortoise.contrib.sanic import register_tortoise


def init_orm(app, config):
    register_tortoise(
        app,
        config=config,
        generate_schemas=True
    )
