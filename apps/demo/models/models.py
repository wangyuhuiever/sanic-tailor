from utils.orm._sqlalchemy import BaseModel
import httpx
import json
from sanic.log import logger as _logger


class DemoModel(BaseModel):
    __tablename__ = 'demo_model'

    async def demo_method(self):
        print('demo method')
