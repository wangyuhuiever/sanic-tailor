from workers.celery_client import app
import logging

_logger = logging.getLogger(__name__)


@app.task(name='schedule_task')
def schedule_task(*args, **kwargs):
    _logger.info({
        'args': args,
        'kwargs': kwargs
    })
    return



