#! -*- coding: utf-8 -*-
import base64
import datetime
import time
import uuid
import random
from passlib.context import CryptContext
from utils.pure_sql.asyncpg import Database
from utils.redis import Redis
from sanic_jwt import Responses, Claim, BaseEndpoint
from sanic_jwt.exceptions import AuthenticationFailed
from sanic.log import logger as _logger
from utils.response import response
from .alisms import Sample

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
    auth_type = request.args.get('type') or 'key'
    basic_string = request.headers.get('Authorization')
    if basic_string:
        base64_string = basic_string.split(' ')[1]
        userinfo = base64.b64decode(base64_string).decode()
        username, password = userinfo.split(':')
    else:
        username = request.json.get('username')
        password = request.json.get('password')

    if not (username and password):
        raise AuthenticationFailed("Missing params.")

    values = {}
    if auth_type == 'email':
        values.update({'email': username, 'password': password})
    elif auth_type == 'phone':
        values.update({'phone': username, 'code': password})
    elif auth_type == 'key':
        values.update({'key': username, 'secret': password})
    else:
        raise AuthenticationFailed("Auth error.")
    auth = await AppUsers(**values).authenticate(auth_type)

    if not auth.get('valid'):
        raise AuthenticationFailed("Auth error.")

    return auth


async def store_refresh_token(request, user_id, refresh_token, *args, **kwargs):
    prefix = Redis.prefix
    key = f'{prefix}refresh_token:{user_id}'
    await request.app.cache.set(key, refresh_token)


async def retrieve_refresh_token(request, user_id, *args, **kwargs):
    prefix = Redis.prefix
    key = f'{prefix}refresh_token:{user_id}'
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


class AppUsers(Database, Redis):
    _name = "app.users"

    _fields = ['id', 'name', 'phone', 'email', 'password', 'key', 'secret', 'code']

    async def create(self, data):
        if data.get('password'):
            data.update({'password': self.hash_password(data.get('password'))})
        user_id = await self.create_single(data)
        return user_id

    async def get_info(self, active=True):
        fields = ['id', 'name', 'phone', 'email', 'password', 'key', 'secret']
        condition = {'active': active}
        if self.phone:
            condition.update({'phone': self.phone})
        elif self.email:
            condition.update({'email': self.email})
        elif self.key:
            condition.update({'key': self.key})
        else:
            return None
        records = await self.search(condition, fields)
        if records:
            return records[0]

    async def send_code(self):
        result = {'success': 0, 'message': None}
        key = f'phone:{self.phone}'
        exist_record = await self.get_code()
        if exist_record:
            # 如果已经有验证码并且发送时间小于一分钟，则不允许再次发送。
            # 如果数据库已经有了，但是用户确实没有收到，可以一分钟后重试，但是需要提前将前一个验证码作废。
            ttl = await self.ttl(key)
            if (180 - ttl) < 60:
                result.update({'message': '请勿频繁发送'})
                return result
        code = str(random.randint(1000, 9999))
        res = await Sample.main_async(self.phone, code)
        try:
            if res.body.code == 'OK':
                _logger.info("发送成功")
            else:
                _logger.error("发送失败: %s" % res.body.message)
                result.update({'message': res.body.message})
                return result
        except Exception as e:
            _logger.error(e)
        await self.set(key, code, ex=180)
        result.update({'success': 1, 'message': '发送成功'})
        return result

    async def get_code(self):
        # redis get
        code = await self.get(f'phone:{self.phone}')
        return code

    async def hash_password(self, password):
        ctx = self._crypt_context()
        f = ctx.hash if hasattr(ctx, 'hash') else ctx.encrypt
        password_hashed = f(password)
        return password_hashed

    async def verify_code(self, code):
        record = await self.get_code()
        return True if code == record else False

    # async def _set_password(self):
    #     password_hashed = await self.hash_password()
    #
    #     sql = f"""
    #     UPDATE app_users SET password=$1 WHERE email=$2 or phone=$3;
    #     """
    #     await self.execute(sql, password_hashed, self.email, self.phone)
    #     return password_hashed

    async def authenticate(self, auth_type):

        # sql = """
        # select id, password from res_users where login=$1;
        # """
        try:

            # result = await Database().execute(sql, self.username)
            record = await self.get_info()
            username = self.name
            valid = False
            if record:
                if auth_type == 'phone':
                    valid = await self.verify_code(self.code)
                elif auth_type == 'email':
                    hashed = record.secret
                    valid, replacement = self._crypt_context().verify_and_update(self.secret, hashed)
                elif auth_type == 'key':
                    valid = False
                    if record.secret == self.secret:
                        valid = True
                if valid:
                    return {'valid': True, 'user_id': record.id, 'username': username}
            return {'valid': False, 'user_id': None, 'username': username}
        except Exception as e:
            _logger.error({
                'authenticate error': e
            })
            return {'valid': False, 'user_id': None, 'username': None}

    def _crypt_context(self):
        """ Passlib CryptContext instance used to encrypt and verify
        passwords. Can be overridden if technical, legal or political matters
        require different kdfs than the provided default.

        Requires a CryptContext as deprecation and upgrade notices are used
        internally
        """
        return default_crypt_context


class Register(BaseEndpoint):
    async def post(self, request, *args, **kwargs):
        result = {'success': 0, 'message': None, 'result': []}
        reg_type = request.args.get('type')
        body = request.json.get('body')
        user_obj = AppUsers()
        if reg_type == 'phone':
            phone = str(body.get('phone'))
            await user_obj.update({'phone': phone})
            record = await user_obj.get_info()
            if record:
                result.update({'message': 'This phone has been register!'})
                return response(result)
            else:
                code = str(body.get('code'))
                values = {'name': phone, 'phone': phone, 'active': True}
                valid = await user_obj.verify_code(code)
                if valid:
                    user_id = await user_obj.create(values)
                else:
                    result.update({'message': 'Verify code failed!'})
                    return response(result)
        elif reg_type == 'email':
            email = body.get('email')
            await user_obj.update({'email': email})
            record = await user_obj.get_info()
            if record:
                result.update({'message': 'This email has been register!'})
                return response(result)
            else:
                password = body.get('password')
                values = {'name': email, 'email': email, 'password': password, 'active': True}
                user_id = await user_obj.create(values)
        else:
            result.update({'message': 'Error type!'})
            return response(result)

        result.update({'success': 1, 'message': 'Register success'})
        return response(result)


class SMSCode(BaseEndpoint):
    async def post(self, request, *args, **kwargs):
        body = request.json.get('body')
        phone = body.get('phone')
        result = await AppUsers(phone=phone).send_code()
        return response(result)

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