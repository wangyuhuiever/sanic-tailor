# -*- coding: utf-8 -*-
import base64
import random
from passlib.context import CryptContext
from utils.redis import Redis
from sanic_jwt import Responses, Claim, BaseEndpoint
from sanic_jwt.exceptions import AuthenticationFailed
from sanic.log import logger as _logger
from utils.response import response
from .alisms import Sample
from utils.orm.db import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, select

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
    auth_type = request.args.get('type') or 'password'
    """
    auth_type: code or password, default is password
    """
    username = ""
    password = ""
    basic_string = request.headers.get('Authorization')
    if basic_string:
        base64_string = basic_string.split(' ')[1]
        userinfo = base64.b64decode(base64_string).decode()
        username, password = userinfo.split(':')

    if not (username and password):
        username = request.json.get('username')
        password = request.json.get('password')

    if not (username and password):
        username = request.args.get('username')
        password = request.args.get('password')

    if not (username and password):
        raise AuthenticationFailed("Missing params.")

    user = None
    async with User.session() as session:
        async with session.begin():
            if auth_type == 'password':
                rec = await session.execute(select(User).filter_by(login=username))
                user = rec.scalar_one_or_none()
            elif auth_type == 'code':
                rec = await session.execute(select(User).filter_by(phone=username))
                user = rec.scalar_one_or_none()
    if not user:
        raise AuthenticationFailed("Wrong username or password!")

    auth = await user.verify(auth_type, password)

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
        raise AuthenticationFailed("No user_id extracted from the token.")

    return payload


class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = {
        "extend_existing": True
    }

    login = Column(String(), unique=True)
    phone = Column(String(), unique=True)
    email = Column(String(), unique=True)
    password_crypt = Column(String())
    active = Column(Boolean(), default=True)

    @property
    def password(self):
        return self.password_crypt

    @password.setter
    def password(self, value):
        password_crypt = self.hash_password(value)
        self.password_crypt = password_crypt

    async def verify_password(self, password):
        valid, replacement = self._crypt_context().verify_and_update(password, self.password_crypt)
        return valid

    async def send_code(self):
        result = {'success': 0, 'message': None}
        key = f'phone:{self.phone}'
        exist_record = await self.get_code()
        if exist_record:
            # 如果已经有验证码并且发送时间小于一分钟，则不允许再次发送。
            # 如果数据库已经有了，但是用户确实没有收到，可以一分钟后重试，但是需要提前将前一个验证码作废。
            ttl = await self.redis.ttl(key)
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
        await self.redis.set(key, code, ex=180)
        result.update({'success': 1, 'message': '发送成功'})
        return result

    async def get_code(self):
        # redis get
        code = await self.redis.get(f'phone:{self.phone}')
        return code

    def hash_password(self, password):
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

    async def verify(self, auth_type, password):

        valid = False
        if auth_type == 'code':
            valid = await self.verify_code(password)
        elif auth_type == 'password':
            valid = await self.verify_password(password)
        if valid:
            return {'valid': True, 'user_id': self.id, 'username': self.name}
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
        result = {'success': 0, 'message': None, 'data': []}
        reg_type = request.args.get('type')
        data = request.json.get('data')
        async with User.session() as session:
            async with session.begin():
                if reg_type == 'code':
                    phone = str(data.get('username'))

                    rec = await session.execute(select(User).filter_by(phone=phone))
                    user = rec.scalar_one_or_none()
                    if user:
                        result.update({'message': 'This phone has been register!'})
                        return response(result)
                    else:
                        code = str(data.get('password'))
                        valid = await User(phone=phone).verify_code(code)
                        if valid:
                            user = User(
                                name=phone,
                                phone=phone,
                                active=True
                            )
                            session.add(user)
                        else:
                            result.update({'message': 'Verify code failed!'})
                            return response(result)
                elif reg_type == 'password':
                    username = data.get('username')
                    rec = await session.execute(select(User).filter_by(login=username))
                    user = rec.scalar_one_or_none()
                    if user:
                        result.update({'message': 'This email has been register!'})
                        return response(result)
                    else:
                        password = data.get('password')
                        user = User(
                            name=username,
                            login=username,
                            password=password,
                            active=True
                        )
                        session.add(user)
                else:
                    result.update({'message': 'Error type!'})
                    return response(result)

        result.update({'success': 1, 'message': 'Register success'})
        return response(result)


class SMSCode(BaseEndpoint):
    async def post(self, request, *args, **kwargs):
        data = request.json.get('data')
        phone = data.get('phone')
        result = await User(phone=phone).send_code()
        return response(result)


class UserInfo(BaseEndpoint):
    async def get(self, request, *args, **kwargs):
        result = {}
        payload = await request.app.ctx.auth.extract_payload(request)
        if not payload:
            raise AuthenticationFailed("No user_id extracted from the token.")
        user_id = payload.get('user_id')
        async with User.session() as session:
            async with session.begin():
                user = await session.get(User, user_id)
        data = {
            'name': user.name,
            'phone': user.phone,
            'email': user.email
        }
        result.update({'data': data, 'success': 1})
        return response(result)

