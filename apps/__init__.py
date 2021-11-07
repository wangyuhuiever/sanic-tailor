def init_apps(app):
    from . import auth
    auth.init_app(app)

    from . import demo
    demo.init_app(app)

    from . import message
    message.init_app(app)