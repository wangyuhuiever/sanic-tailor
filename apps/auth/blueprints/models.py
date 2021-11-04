from sanic import Blueprint
from sanic.log import logger
from utils.response import response
from decorators.error import catch_user_exception
from apps.auth.models.users import User

auth = Blueprint("Auth")


@auth.route("/test", methods=['GET'])
@catch_user_exception
async def test_api(request):
    headers = request.headers
    logger.info({'headers': headers})

    t1 = await User.create(name='table')
    print(t1)

    return response({'data': '1'})

