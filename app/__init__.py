from starlette.applications import Starlette

import settings
from .routes import routes
from .extensions import starchart, extensions
from .exception_handlers import handlers
from .middleware import middleware
from .models import MODELS


__all__ = ["create_app"]


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

    for M in MODELS:
        starchart.schema_generator.add_schema(M.__name__, M.schema())

    return app
