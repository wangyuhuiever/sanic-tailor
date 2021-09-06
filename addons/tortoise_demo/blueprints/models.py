from sanic import Blueprint
from sanic.log import logger
from misc.response import response
from decorators.error import catch_user_exception
from addons.tortoise_demo.models.orm_models import DemoORMModel

api = Blueprint("Tortoise Demo Api")


@api.route("/orm/test", methods=['POST'])
@catch_user_exception
async def test_api(request):
    headers = request.headers
    logger.info({'headers': headers})

    data = await DemoORMModel.create(**{
        'col1': 1,
        'col2': 'jakflkjklff'
    })

    res = await DemoORMModel.filter(id=data.id).first().values()
    return response({'data': res})
