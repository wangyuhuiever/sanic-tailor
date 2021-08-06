# -*- coding: utf-8 -*-
from workers import app
from utils.db import AnotherDatabase

database = AnotherDatabase(
    app.conf.custom_db_host,
    app.conf.custom_db_port,
    app.conf.custom_db_user,
    app.conf.custom_db_pass,
    app.conf.custom_db_name,
)