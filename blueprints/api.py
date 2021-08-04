from sanic import Blueprint
from sanic.log import logger
from misc.response import response
from decorators.database import insert_database
from decorators.error import catch_user_exception

api = Blueprint("Api")


@api.route("/test", methods=['POST'])
@insert_database
@catch_user_exception
async def test_api(request, database):
    headers = request.headers
    logger.info({'headers': headers})

    sql = "insert into test_table (col1, col2) values ($1, $2) returning id;"
    values = [1, 'test']
    res = await database.execute(sql, *values)

    data = [dict(r) for r in res]
    return response({'data': data})
