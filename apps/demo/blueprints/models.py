from sanic import Blueprint
from sanic.log import logger
from utils.response import response
from decorators.error import catch_user_exception
from apps.demo.models.models import DemoModel
from utils.rpc.server import register_rpc

api = Blueprint("Demo Api")


@api.route("/test", methods=['POST'])
@catch_user_exception
@register_rpc('test_api')
async def test_api(request):
    headers = request.headers
    logger.info({'headers': headers})

    data = await DemoModel().insert_data()

    return response({'data': data})

