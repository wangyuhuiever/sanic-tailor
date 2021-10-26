from sanic import Sanic
from sanic_cors import CORS
from addons import api
import settings
from utils import init_utils

app = Sanic(settings.Sanic.name)
app.update_config(settings.Sanic)
app.blueprint(api)

CORS(app)
init_utils(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, workers=8, access_log=True, auto_reload=False)