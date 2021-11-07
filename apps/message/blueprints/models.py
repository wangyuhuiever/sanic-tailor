# -*- coding: utf-8 -*-
from sanic import Blueprint
from sanic_jwt import protected, inject_user
from sanic.log import logger as _logger
from ..tools.chats import message_send as chat_message_send
from utils.response import response

api = Blueprint("Message")


@api.route('/sessions', methods=['GET'])
@protected()
async def message_sessions(request):
    sessions = request.app.message
    _logger.info({'sessions': sessions})
    result = {'success': 1, 'data': sessions}
    return response(result)


@api.route('/send', methods=['POST'])
@protected()
@inject_user()
async def message_send(request, user):
    body = request.json.get('body')

    await chat_message_send(user.get('user_id'), body)
    result = {}
    result.update({'success': 1})
    return response(result)