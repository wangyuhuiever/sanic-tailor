# -*- coding: utf-8 -*-
import asyncio
import datetime
from sanic_jwt import Initialize
from sanic.log import logger as _logger
from .users import authenticate, store_refresh_token, retrieve_refresh_token, retrieve_user, Register, SMSCode,\
    UserInfo, default_crypt_context
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from settings import ORM
engine = create_async_engine(
    "{db_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(
        db_driver=ORM.SQLAlchemy.db_driver,
        db_user=ORM.SQLAlchemy.db_user,
        db_pass=ORM.SQLAlchemy.db_pass,
        db_host=ORM.SQLAlchemy.db_host,
        db_port=ORM.SQLAlchemy.db_port,
        db_name=ORM.SQLAlchemy.db_name,
    ),
    echo=True
)


def init_app(app):
    _logger.info("Auth Initialize...")
    Initialize(
        app,
        url_prefix='/api',
        path_to_authenticate='/auth',
        path_to_refresh='/refresh',
        path_to_verify='/verify',
        authenticate=authenticate,
        refresh_token_enabled=True,
        store_refresh_token=store_refresh_token,
        retrieve_refresh_token=retrieve_refresh_token,
        retrieve_user=retrieve_user,
        class_views=[
            ('/register', Register),
            ('/send_code', SMSCode),
            ('/user/info', UserInfo),
        ]
    )
    asyncio.run(insert_admin())


async def insert_admin():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT id FROM users WHERE login=:login or id=:id"), {"login": "admin", "id": 1})
        user = list(res)
        if not user:
            ctx = default_crypt_context
            f = ctx.hash if hasattr(ctx, 'hash') else ctx.encrypt
            password_hashed = f("admin")
            now = datetime.datetime.utcnow()
            await conn.execute(text("""INSERT INTO users (name, login, password_crypt, active, create_date, write_date)
             values (:name, :login, :password_crypt, :active, :create_date, :write_date)"""), {
                "name": "Administrator",
                "login": "admin",
                "password_crypt": password_hashed,
                "active": True,
                "create_date": now,
                "write_date": now
            })
        await conn.commit()