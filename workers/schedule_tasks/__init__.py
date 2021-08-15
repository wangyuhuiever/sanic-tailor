from workers import app
from .models import schedule_task, cron_task
from celery.schedules import crontab


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    # 每10秒触发一次
    sender.add_periodic_task(10, schedule_task.s('args: ', '1', '2', kwarg='kwarg', kwarg2='kwarg2'))

    # 每天10点30触发一次
    sender.add_periodic_task(
        crontab(hour=10, minute=30),
        cron_task.s('cron args:', '1', '2', kwarg='kwarg')
    )

