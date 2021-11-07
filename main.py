from sanic import Sanic
from sanic_cors import CORS
from apps import init_apps
import settings
from utils import init_utils
# import logging
#
# logger = logging.getLogger('tortoise')
# logger.setLevel(logging.DEBUG)

app = Sanic(settings.Sanic.name)
app.update_config(settings.Sanic)

CORS(app)
init_utils(app)
init_apps(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8422, workers=8, access_log=False, auto_reload=False)