from starlette.applications import Starlette

import settings
from .routes import routes
from .extentions import extensions
from .exception_handlers import handlers
from .middleware import middleware


def create_app():
    app = Starlette()
    app.debug = settings.DEBUG

    for m in middleware:
        app.add_middleware(m)

    app.routes.extend(routes)

    for ext in extensions:
        ext.register(app)

    for handler in handlers:
        app.add_exception_handler(handler.EXC, handler.handle)

    return app
