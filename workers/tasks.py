from workers.celery_client import app


@app.task(name='sum')
def sum(x, y):
    return x + y




