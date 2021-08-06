# -*- coding: utf-8 -*-
import os
import time
import settings
from threading import Thread
from subprocess import Popen, PIPE
from sanic.log import logger as _logger


class CeleryJob(object):

    def __init__(self, app):
        self.restart = True
        self.app = app

    def poll(self):
        return None

    def start_celery(self, path):
        if self.restart:
            p = Popen(
                [
                    "celery",
                    "-A",
                    "workers",
                    "worker",
                    "--loglevel=info",
                    "-n",
                    "worker1.%n[{}] {}".format(self.app.name, self.app.__hash__()),
                    "-B",
                    "-s",
                    "/tmp/celerybeat-schedule"
                ],
                cwd=path, stdin=PIPE
            )
            return p
        else:
            return self

    def start_flower(self, path):
        if self.restart:
            f = Popen(
                [
                    "celery",
                    "-A",
                    "workers",
                    "flower",
                    "--port=%s" % settings.Celery.custom_flower_port or '5555',
                    "--basic_auth=%s:%s" % (settings.Celery.custom_flower_user or 'admin', settings.Celery.custom_flower_pass or 'admin'),
                ],
                cwd=path, stdin=PIPE
            )
            return f
        else:
            return self

    def check_status(self):
        path = os.path.abspath(os.path.dirname(__name__))
        c = self.start_celery(path)
        f = self.start_flower(path)
        while 1:
            if c.poll() is not None:
                c = self.start_celery(path)
            if f.poll() is not None:
                f = self.start_flower(path)
            time.sleep(10)

    def run(self):
        thr = Thread(name='celery_thread', target=self.check_status)
        thr.daemon = True
        thr.start()

    def stop(self):
        Popen(['pkill', '-f', 'celery'])
        self.restart = False


async def init_celery(app, loop):
    _logger.info("Celery starting...")
    celery_thread = CeleryJob(app)
    celery_thread.run()
    app.celery = celery_thread


async def close_celery(app, loop):
    _logger.info("Celery stopping...")
    app.celery.stop()
