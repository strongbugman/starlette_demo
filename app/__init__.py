from importlib import import_module

from starlette.applications import Starlette as _Starlette

import settings
from .routes import ROUTES
from .extensions import EXTENSIONS
from .exception_handlers import HANDLERS
from .middleware import MIDDLEWARE


__all__ = ["create_app"]


class Starlette(_Starlette):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started = False

    async def startup(self):
        if not self.started:
            await self.router.lifespan.startup()
            self.started = True

    async def shutdown(self):
        if self.started:
            await self.router.lifespan.shutdown()
            self.started = False


def create_app():
    app = Starlette()
    app.debug = settings.DEBUG

    for m in MIDDLEWARE:
        app.add_middleware(m)

    app.routes.extend(ROUTES)

    for ext in EXTENSIONS:
        ext.register(app)

    for handler in HANDLERS:
        app.add_exception_handler(handler.EXC, handler.handle)

    import_module("app.tasks")

    return app
