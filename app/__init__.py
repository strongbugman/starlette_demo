from importlib import import_module

from starlette.applications import Starlette

import settings
from .routes import ROUTES
from .extensions import starchart, EXTENSIONS
from .exception_handlers import HANDLERS
from .middleware import MIDDLEWARE
from .models import MODELS


__all__ = ["create_app"]


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

    for M in MODELS:
        starchart.schema_generator.add_schema(M.__name__, M.schema())
        starchart.schema_generator.add_schema(
            f"{M.__name__}s",
            {
                "type": "object",
                "properties": {
                    "objects": {
                        "type": "array",
                        "items": {"$ref": f"#/components/schemas/{M.__name__}"},
                    },
                    "page": {"type": "integer"},
                    "count": {"type": "integer"},
                },
            },
        )

    import_module("app.tasks")

    return app
