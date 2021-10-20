from functools import wraps
from sanic.log import logger
from utils.response import response


def catch_user_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            res = await func(*args, **kwargs)
        except Exception as e:
            results = {'error': str(e), 'success': 0}
            logger.error({
                '程序异常': e
            })
            return response(results, status=500)
        return res

    return wrapper
