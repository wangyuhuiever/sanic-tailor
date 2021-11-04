from sanic import Blueprint
from sanic.log import logger
from utils.response import response
from decorators.error import catch_user_exception
from utils.orm._sqlalchemy import Models  # 无需import具体class，通过Models查询，可以使用_inherit继承特性
from utils.rpc.server import register_rpc

api = Blueprint("Demo Api")


@api.route("/test", methods=['POST'])
@catch_user_exception
@register_rpc('test_api')
async def test_api(request):
    headers = request.headers
    logger.info({'headers': headers})

    model = Models.get('demo.model')
    await model().demo_method()

    return response({'data': '1'})

