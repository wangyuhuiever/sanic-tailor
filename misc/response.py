# -*- coding: utf-8 -*-
from decimal import Decimal
from sanic.response import json as sanic_json
import datetime
import json


class DataToJSON(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            dt = o + datetime.timedelta(hours=8)  # utc强制转 +8
            return dt.__str__()
        elif isinstance(o, Decimal):
            return float(o)
        return json.JSONEncoder.default(self, o)


def response(*args, **kwargs):
    return sanic_json(dumps=json.dumps, ensure_ascii=False, cls=DataToJSON, *args, **kwargs)