#! -*- coding: utf-8 -*-
from settings import Auth
from sanic_jwt import Initialize
from sanic.log import logger as _logger
from .users import authenticate, store_refresh_token, retrieve_refresh_token, retrieve_user, Register, SMSCode, UserInfo


def init_auth(app):
    _logger.info("Auth Initialize...")
    Initialize(
        app,
        url_prefix='/api',
        path_to_authenticate='/auth',
        path_to_refresh='/refresh',
        path_to_verify='/verify',
        secret=Auth.secret,
        authenticate=authenticate,
        refresh_token_enabled=True,
        expiration_delta=Auth.expiration_delta,
        store_refresh_token=store_refresh_token,
        retrieve_refresh_token=retrieve_refresh_token,
        retrieve_user=retrieve_user,
        class_views=[
            ('/register', Register),
            ('/send_code', SMSCode),
            ('/user/info', UserInfo),
        ]
    )