from functools import wraps


def insert_database(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        database = request.app.database
        res = await func(request, database, *args, **kwargs)
        return res
    return wrapper

