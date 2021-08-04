# -*- coding: utf-8 -*-
from celery import Celery
import settings

broker = 'amqp://%s:%s@%s:%s/%s' % (
    settings.MQ_USER, settings.MQ_PASS, settings.MQ_HOST, settings.MQ_PORT, settings.MQ_VHOST)

backend = 'redis://default:%s@%s:%s/%s' % (
    settings.REDIS_PASS, settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)

app = Celery('Workers', broker=broker, backend=backend, include=['workers.tasks', 'workers.schedule_tasks'])

app.conf.beat_schedule = {
    'schedule_task_log': {
        'task': 'schedule_task',
        'schedule': 60 * 2,
        'args': (1, 2),
        'kwargs': {'a': 'a'}
    }
}

app.conf.update(
    result_expires=3600,
    enable_utc=True,
)

if __name__ == '__main__':
    app.start()
