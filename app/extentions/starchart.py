from functools import partial

from starchart import SchemaGenerator, SwaggerUI, Schema

import settings
from .base import Extension


class Starchart(Extension):
    def __init__(self):
        super().__init__()
        self.schema_generator = SchemaGenerator(
            title=settings.STARCHART_TITLE,
            description=settings.STARCHART_DESCRIPTION,
            version=settings.STARCHART_VERSION,
            openapi_version=settings.STARCHART_OPENAPI_VERSION,
        )
        SwaggerUI.set_schema_url(settings.STARCHART_SCAHMA_PATH)
        self.schema_generator.add_schema(
            "Cat",
            {
                "properties": {
                    "code": {"description": "global unique", "type": "string"},
                    "name": {"description": "global unique", "type": "string"},
                },
                "type": "object",
            },
        )

    def startup(self):
        self.schema_generator.load_schema(self.app.routes)
        Schema.set_schema_loader(
            partial(self.schema_generator.get_schema, self.app.routes)
        )

        self.app.add_route(
            settings.STARCHART_SCAHMA_PATH,
            Schema,
            methods=["GET"],
            name="SwaggerSchema",
            include_in_schema=False,
        )
        self.app.add_route(
            settings.STARCHART_UI_PATH,
            SwaggerUI,
            methods=["GET"],
            name="SwaggerUI",
            include_in_schema=False,
        )
        self.app.schema_generator = self.schema_generator
