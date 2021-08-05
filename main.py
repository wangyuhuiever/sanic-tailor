from sanic import Sanic
from blueprints import bp
from utils.database import init_database, close_database
from utils.celery import celery_start, celery_stop
import settings

app = Sanic(settings.Sanic.name)
app.update_config(settings.Sanic)
app.blueprint(bp)

app.register_listener(init_database, 'before_server_start')
app.register_listener(close_database, 'after_server_stop')

app.register_listener(celery_start, 'main_process_start')
app.register_listener(celery_stop, 'main_process_stop')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, workers=8, access_log=True, auto_reload=False)