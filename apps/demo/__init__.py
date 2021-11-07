from sanic.log import logger as _logger


def init_app(app):
    _logger.info("Demo Initialize...")

    from .blueprints import demo_api
    app.blueprint(demo_api, url_prefix='/api')