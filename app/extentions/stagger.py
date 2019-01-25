import typing
from collections import defaultdict
from functools import partial
import json

from starlette.schemas import BaseSchemaGenerator
from starlette.routing import BaseRoute
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import TemplateResponse, JSONResponse
from jinja2 import Template
import yaml
from webargs.asyncparser import AsyncParser

import settings
from .base import Extension


class Parser(AsyncParser):
    __location_map__ = AsyncParser.__location_map__.update(
        path_params="parse_path_params"
    )


class SchemaGenerator(BaseSchemaGenerator):
    SWAGGER_PATH_ATTR_NAME = "__swagger_path__"

    def __init__(
        self,
        title: str = "Stagger",
        version: str = "0.1",
        description: str = "Api document",
        openapi_version: str = "2.0",
    ):
        self.schema: typing.Dict = {
            "info": {"title": title, "description": description, "version": version},
            "definitions": {},
            "paths": defaultdict(dict),
        }
        if openapi_version == "2.0":
            self.schema["swagger"] = openapi_version
        else:
            self.schema["openapi"] = openapi_version
        self.loaded = False

    @staticmethod
    def load_document(file_path: str) -> typing.Dict:
        with open(file_path) as f:
            if file_path.endswith("json"):
                return json.load(f)
            else:
                return yaml.safe_load(f)

    def add_definition(self, name, definition):
        self.schema["definitions"][name] = definition

    def add_path(self, path: str, method: str, document: typing.Dict):
        self.schema["paths"][path][method] = document

    def load_schema(self, routes: typing.List[BaseRoute]):
        for endpoint in self.get_endpoints(routes):
            doc_path: typing.Optional[str] = getattr(
                endpoint.func, self.SWAGGER_PATH_ATTR_NAME, None
            )

            if doc_path:
                doc = self.load_document(doc_path)
            else:
                doc = self.parse_docstring(endpoint.func)

            self.add_path(endpoint.path, endpoint.http_method, doc)

        self.loaded = True

    def get_schema(self, routes: typing.List[BaseRoute]) -> typing.Dict:
        if not self.loaded:
            self.load_schema(routes)
        return self.schema

    def swagger_from(self, file_path: str) -> typing.Callable:
        def decorator(func: typing.Callable) -> typing.Callable:
            setattr(func, self.SWAGGER_PATH_ATTR_NAME, file_path)
            return func

        return decorator


class UI(HTTPEndpoint):
    TEMPLATE = Template(open("./app/static/index.html").read())
    CONTEXT = {
        "title": "Swagger UI",
        "swagger_ui_css": "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.20.5"
        "/swagger-ui.css",
        "swagger_ui_bundle_js": "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3"
        ".20.5/swagger-ui-bundle.js",
        "swagger_ui_standalone_preset_js": "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.20.5/swagger-ui-standalone-preset.js",
        "schema_url": "./schema/",
        "request": None,
    }

    def get(self, res: Request):
        self.CONTEXT["request"] = res
        return TemplateResponse(self.TEMPLATE, self.CONTEXT)


class Schema(HTTPEndpoint):
    SCHEMA_LOADER: typing.Callable[[], typing.Dict] = lambda: dict

    def get(self, res: Request):
        return JSONResponse(self.SCHEMA_LOADER())


class Stagger(Extension):
    def __init__(self):
        super().__init__()
        self.schema_generator = SchemaGenerator(
            title=settings.STAGGER_TITLE,
            description=settings.STAGGER_DESCRIPTION,
            version=settings.STAGGER_VERSION,
            openapi_version=settings.STAGGER_OPENAPI_VERSION,
        )
        UI.CONTEXT["schema_url"] = settings.STAGGER_SCAHMA_PATH
        UI.TEMPLATE = Template(open(settings.STAGGER_UI_INDEX_FILE).read())
        self.schema_generator.add_definition(
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
        Schema.SCHEMA_LOADER = partial(
            self.schema_generator.get_schema, self.app.routes
        )

        self.app.add_route(
            settings.STAGGER_SCAHMA_PATH,
            Schema,
            methods=["GET"],
            name="SwaggerSchema",
            include_in_schema=False,
        )
        self.app.add_route(
            settings.STAGGER_UI_PATH,
            UI,
            methods=["GET"],
            name="SwaggerUI",
            include_in_schema=False,
        )
        self.app.schema_generator = self.schema_generator
