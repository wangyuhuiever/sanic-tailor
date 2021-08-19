from sanic import Sanic
from addons import api
import settings
from utils import init_utils

app = Sanic(settings.Sanic.name)
app.update_config(settings.Sanic)
app.blueprint(api)

init_utils(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, workers=8, access_log=True, auto_reload=False)