from .. import sio, MESSAGE_SESSIONS
from socketio.exceptions import SocketIOError
from sanic.log import logger as _logger
from utils.orm.db import Models


@sio.on("public send")
async def public_send(sid, data):
    sio.emit("public", data)


# 客户端监听public事件，服务端发送公共消息至此event
# @sio.on('public')
# async def public(sid, data):
#     pass


@sio.on("message send")
async def message_send(sid, data):
    """
    Server send message to `message receive` event
    :param sid: user session id or user_id form internal
    :param data: receive from client:{
        "receiver_id": user_id,
        "message": json string
    }
    """
    content = data.get('message')
    receiver_id = data.get('receiver_id')
    if isinstance(sid, int):
        user_id = sid
    else:
        session = await sio.get_session(sid)
        user_id = session['user_id']
    Message = Models.get('messages')
    MessageContent = Models.get('message.contents')
    user_value = {
        "create_uid": user_id,
        "write_uid": user_id
    }
    async with MessageContent.session() as session:
        async with session.begin():
            value = dict(
                content=content,
                **user_value
            )
            message_content = MessageContent(
                **value
            )
            session.add(message_content)

    async with Message.session() as session:
        async with session.begin():
            value = dict(
                content_id=message_content.id,
                receiver_id=receiver_id,
                **user_value
            )
            message = Message(
                **value
            )
            session.add(message)
    receiver_sessions = MESSAGE_SESSIONS[receiver_id]
    if receiver_sessions:
        for receiver_session in receiver_sessions:
            await sio.emit("message receive", data, receiver_session)


# 此方法客户端实现，服务端发送消息至此event
# @sio.on('message receive')
# async def message_receive(sid, data):
#     pass


@sio.on('room message send')
async def room_message_send(sid, data):
    pass


# 此方法客户端实现，服务端发送room消息至此event
# @sio.on('room message receive')
# async def room_message_receive(sid, data):
#     pass


# @sio.on('*')
# async def catch_all(event, sid, data):
#     pass