from sanic.log import logger as _logger
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declared_attr
from sqlalchemy import BigInteger, Column, ForeignKey, String, DateTime, text
from sqlalchemy.orm import declarative_base, relationship
import datetime
from settings import ORM

db = create_async_engine(
    "postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(
        db_user=ORM.SQLAlchemy.db_user,
        db_pass=ORM.SQLAlchemy.db_pass,
        db_host=ORM.SQLAlchemy.db_host,
        db_port=ORM.SQLAlchemy.db_port,
        db_name=ORM.SQLAlchemy.db_name,
    ),
    echo=True
)


def init_sqlalchemy(app, config):
    _logger.info("sqlalchemy starting...")
    app.update_config(config)

    _base_model_session_ctx = ContextVar("session")

    @app.middleware("request")
    async def inject_session(request):
        request.ctx.session = sessionmaker(db, AsyncSession, expire_on_commit=False)()
        request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)

    @app.middleware("response")
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger(), primary_key=True, autoincrement=True)

    @declared_attr
    def create_uid(self):
        return Column(BigInteger(), ForeignKey('users.id'))

    create_date = Column(DateTime(), nullable=False, default=datetime.datetime.utcnow())

    @declared_attr
    def write_uid(self):
        return Column(BigInteger(), ForeignKey('users.id'))
    write_date = Column(DateTime(), nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    session = sessionmaker(db, AsyncSession, expire_on_commit=False)

    async def execute(self, sql, values):
        with db.connect() as conn:
            result = conn.execute(
                text(sql, values)
            )
        return result


class BaseUser(BaseModel):
    __tablename__ = 'users'

    name = Column(String(), nullable=False)


from apps.auth import __models__
