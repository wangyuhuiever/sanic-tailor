from .server import RPC
from sanic.log import logger as _logger


def init_rpc(app):
    _logger.info("RPC Initialize...")
    RPC(
        app
    )