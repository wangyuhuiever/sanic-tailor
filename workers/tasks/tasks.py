# -*- coding: utf-8 -*-
from workers import app


@app.task(name='sum')
def sum(x, y):
    return x + y




