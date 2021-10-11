#! -*- coding: utf-8 -*-
from sanic_jwt import Initialize
from .models import authenticate, store_refresh_token, retrieve_refresh_token, retrieve_user


def init_auth(app):
    Initialize(
        app,
        url_prefix='/api',
        path_to_authenticate='/auth',
        path_to_refresh='/refresh',
        path_to_verify='/verify',
        secret='hard to guess',
        authenticate=authenticate,
        refresh_token_enabled=True,
        expiration_delta=60 * 60 * 24,
        store_refresh_token=store_refresh_token,
        retrieve_refresh_token=retrieve_refresh_token,
        retrieve_user=retrieve_user,
        # class_views=[
        #     ('/register', UserRegisterHandler)
        # ]
    )