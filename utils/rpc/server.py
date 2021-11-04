from utils.response import response
from sanic_jwt import protected
from functools import wraps
from utils.orm._sqlalchemy import Models
from sanic.log import logger as _logger
from sanic.exceptions import SanicException
from decorators.error import catch_user_exception

FUNCTION_MAPPINGS = {}


def register_rpc(func_id):
    def wrapper(func):
        if func_id in FUNCTION_MAPPINGS:
            raise SanicException(f"Duplicate ID: {func_id}!")
        FUNCTION_MAPPINGS.update({func_id: func})
        @wraps(func)
        async def decorate(*args, **kwargs):
            res = await func(*args, **kwargs)
            return res
        return decorate
    return wrapper


class RPC(object):

    def __init__(self, app, path=None, *args, **kwargs):
        self.app = app
        self.path = path or '/jsonrpc'
        self.ping = self.path + '/ping'

        self._add_route()

    def _add_route(self):
        self.app.add_route(process_start, self.path, methods=['POST'])
        self.app.add_route(rpc_ping, self.ping, methods=['GET'])


@protected()
@catch_user_exception
async def process_start(request):
    result = {'success': 0, 'error': None, 'data': None}
    body = request.json
    if not body:
        result.update({'error': "Missing Params!"})
        return response({result}, status=411)
    type = body.get('type')
    name = body.get('name')
    args = body.get('args') or []
    kwargs = body.get('kwargs') or {}

    try:
        if type == 'request':
            res = await FUNCTION_MAPPINGS[name](request, *args, **kwargs)
        elif type == 'model':
            model = body.get('model')
            # model_id = body.get('id')
            # model_ids = body.get('ids')
            model_obj = Models.get(model)
            self = await model_obj.model()  # todo: 使用orm查询出record
            res = await model_obj.get_function(name).function(self, *args, **kwargs)
        else:
            result.update({'error': 'Wrong Type!'})
            return response(result)
    except KeyError as e:
        _logger.info({"error": e})
        result.update({'error': 'Function name not exist!'})
        return response(result)
    except Exception as e:
        _logger.info({"error": e})
        result.update({'error': 'Internal Error!'})
        return response(result)
    result.update({'success': 1, 'data': res})
    return response(result)


@catch_user_exception
async def rpc_ping(request):
    return response({'ping': 'pong'})
