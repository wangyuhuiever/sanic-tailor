from sanic import Blueprint
from sanic.log import logger
from misc.response import response
from decorators.error import catch_user_exception
from blueprints.demo.models.models import DemoModel

api = Blueprint("Api")


@api.route("/test", methods=['POST'])
@catch_user_exception
async def test_api(request):
    headers = request.headers
    logger.info({'headers': headers})

    res = await DemoModel().insert_data()

    data = [dict(r) for r in res]
    return response({'data': data})