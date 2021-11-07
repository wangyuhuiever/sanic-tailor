# -*- coding: utf-8 -*-
from sanic.log import logger as _logger
from sanic_jwt.exceptions import AuthenticationFailed
import socketio
sio = socketio.AsyncServer(async_mode='sanic')

MESSAGE_SESSIONS = {
    # "user_id": ["sid"]
}


async def authenticate_user(app, auth):
    if not auth:
        raise AuthenticationFailed("No user_id extracted from the token.", status_code=200)
    token = auth.split(' ')[1]
    payload = await app.ctx.auth._decode(token)
    if not payload:
        raise AuthenticationFailed("No user_id extracted from the token.", status_code=200)
    return payload


def init_app(app):
    _logger.info("Message Initialize...")
    sio.attach(app)
    global MESSAGE_SESSIONS
    app.message = MESSAGE_SESSIONS

    @sio.event
    async def connect(sid, environ, auth):
        payload = await authenticate_user(app, auth)
        user_id = payload.get('user_id')
        role = payload.get('role')
        global MESSAGE_SESSIONS
        MESSAGE_SESSIONS.setdefault(user_id, [])
        MESSAGE_SESSIONS[user_id].append(sid)
        await sio.save_session(sid, {'user_id': user_id, 'role': role})

    @sio.event
    async def disconnect(sid):
        global MESSAGE_SESSIONS
        session = await sio.get_session(sid)
        user_id = session['user_id']
        MESSAGE_SESSIONS[user_id].remove(sid)

    from .tools import chats

    from .blueprints import message_api
    app.blueprint(message_api, url_prefix='/api')