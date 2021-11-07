from sanic.log import logger as _logger
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declared_attr
from sqlalchemy import BigInteger, Column, ForeignKey, String, DateTime, text
from sqlalchemy.orm import declarative_base, relationship
import datetime
import inspect
from settings import ORM
try:
    from utils.redis import Redis
    rdb = Redis().redis
except:
    rdb = None

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
    _logger.info("SQLAlchemy starting...")
    app.update_config(config)
    _set_up_models(BaseModel)

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
    redis = rdb

    async def execute(self, sql, values):
        with db.connect() as conn:
            result = conn.execute(
                text(sql, values)
            )
        return result


class User(BaseModel):
    __tablename__ = 'users'

    name = Column(String(), nullable=False)


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
        return models[0].model if models else cls

    def get_function(self, name):
        functions = list(filter(lambda r: r.model == self.model and r.name == name, FUNCTION_RECORDS))
        return functions[0].function if functions else None


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
        # 所有抽象类不注册，无 __tablename__则认为是抽象类
        if subclass.__tablename__:
            # 1. 如果类名已经注册，则需要注册更基础的子类，同时增加子类的__bases__
            # 2. 如果类名尚未注册，则直接注册
            subclass_name = getattr(subclass, '_name', None)
            if not subclass_name:
                subclass_name = subclass.__tablename__.replace('_', '.')

            if subclass_name in all_classes.keys():
                old_class = all_classes[subclass_name]
                bases = old_class.__bases__
                new_bases = list(bases)
                if old_class not in new_bases:
                    new_bases.insert(0, old_class)
                subclass.__bases__ = tuple(new_bases)

            # 如果该类有继承非当前类名的类，同样需要增加__base__
            inherit_name = getattr(subclass, '_inherit', None)
            if inherit_name and inherit_name != subclass_name:
                bases = subclass.__bases__
                new_bases = list(bases)
                if all_classes[inherit_name] not in new_bases:
                    new_bases.insert(0, all_classes[inherit_name])
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



from apps import __model_install__
