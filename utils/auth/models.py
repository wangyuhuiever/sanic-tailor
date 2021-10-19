#! -*- coding: utf-8 -*-
import base64
import datetime
import time
import uuid
from passlib.context import CryptContext
from utils.pure_sql.asyncpg import Database
from sanic_jwt import Responses, Claim
from sanic_jwt.exceptions import AuthenticationFailed
from sanic.log import logger as _logger

default_crypt_context = CryptContext(
    # kdf which can be verified by the context. The default encryption kdf is
    # the first of the list
    ['pbkdf2_sha512', 'plaintext'],
    # deprecated algorithms are still verified as usual, but ``needs_update``
    # will indicate that the stored hash should be replaced by a more recent
    # algorithm. Passlib 1.6 supports an `auto` value which deprecates any
    # algorithm but the default, but Ubuntu LTS only provides 1.5 so far.
    deprecated=['plaintext'],
)


# async def extend_payload(payload, *args, **kwargs):
#     return payload


async def authenticate(request, *args, **kwargs):
    # 1. 尝试从 header 的 Authorization 中获取用户名密码
    # 2. 尝试从 post body 中获取用户名密码
    # 3. 尝试从 url params 中获取用户名密码
    # 如果还是获取不到就提示信息缺少

    basic_string = request.headers.get('Authorization')
    if basic_string:
        base64_string = basic_string.split(' ')[1]
        userinfo = base64.b64decode(base64_string).decode()
        username, password = userinfo.split(':')
    else:
        username = request.json.get('username')
        password = request.json.get('password')

    if not (username and password):
        username = request.args.get('username')
        password = request.args.get('password')

    if not (username and password):
        raise AuthenticationFailed("Missing params.")

    auth = await AuthUsers(username, password).authenticate()

    if not auth.get('valid'):
        raise AuthenticationFailed("Auth error.")

    return auth


async def store_refresh_token(request, user_id, refresh_token, *args, **kwargs):
    key = f'refresh_token:{user_id}'
    await request.app.cache.set(key, refresh_token)


async def retrieve_refresh_token(request, user_id, *args, **kwargs):
    key = f'refresh_token:{user_id}'
    return request.app.cache.get(key)


async def retrieve_user(request, *args, **kwargs):
    """
    获取用户信息
    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    payload = await request.app.ctx.auth.extract_payload(request)
    if not payload:
        raise AuthenticationFailed("No user_id extracted from the token.", status_code=200)

    return payload


class AuthUsers(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    async def authenticate(self):

        sql = """
        select id, password from res_users where login=$1; 
        """
        try:

            result = await Database().execute(sql, self.username)

            if result:
                hashed = result[0]['password']
                valid, replacement = self._crypt_context().verify_and_update(self.password, hashed)
                if valid:
                    return {'valid': True, 'user_id': result[0].get('id'), 'username': self.username}
            return {'valid': False, 'user_id': None, 'key': self.username}
        except Exception as e:
            _logger.error({
                'authenticate error': e
            })
            return {'valid': False, 'user_id': None, 'username': self.username}

    def _crypt_context(self):
        """ Passlib CryptContext instance used to encrypt and verify
        passwords. Can be overridden if technical, legal or political matters
        require different kdfs than the provided default.

        Requires a CryptContext as deprecation and upgrade notices are used
        internally
        """
        return default_crypt_context


# class SubClaim(Claim):
#     key = 'sub'
#
#     def setup(self, payload, user):
#         return user.get('key')
#
#     def verify(self, value):
#         return True
#
#
# class CustomResponse(Responses):
#     @staticmethod
#     def extend_authenticate(
#         request, user=None, access_token=None, refresh_token=None
#     ):
#
#         async def insert_user_token():
#             payload = await request.app.ctx.auth._decode(access_token)
#             sql = """
#             insert into app_token (user_id, access_token, expiry_time, active, refresh_token, create_uid, create_date, write_uid, write_date)
#             values ($1, $2, $3, $4, $5, $6, $7, $8, $9);
#             """
#             time_now = datetime.datetime.utcnow()
#             values = [
#                 user.get('uid'),
#                 access_token,
#                 datetime.datetime.fromtimestamp(payload.get('exp'), datetime.timezone.utc).replace(tzinfo=None),
#                 True,
#                 refresh_token,
#                 1,
#                 time_now,
#                 1,
#                 time_now
#             ]
#             await Database().execute(sql, *values)
#
#
#         request.app.add_task(insert_user_token())
#
#         return {'expiresIn': request.app.config.TOKEN_EXPIRE_TIME}
#
#     @staticmethod
#     def extend_retrieve_user(request, user=None, payload=None):
#         expiry = int(payload.get('exp') - time.time())
#         return {'expiresIn': expiry}