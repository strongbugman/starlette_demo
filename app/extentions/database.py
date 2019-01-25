import typing

from tortoise import Tortoise
from tortoise.models import Model
from tortoise.backends.base.client import BaseDBAsyncClient

import settings
from .base import Extension


class DBExtension(Extension):
    MODEL_PATH = ["app.models"]

    @property
    def models(self) -> typing.Set[typing.Type[Model]]:
        return set(Tortoise.apps[settings.PROJECT_NAME].values())

    @property
    def _connection(self) -> BaseDBAsyncClient:
        return Tortoise._connections["default"]

    async def startup(self):
        await Tortoise.init(
            db_url=settings.DB_URL, modules={settings.PROJECT_NAME: self.MODEL_PATH}
        )

    async def shutdown(self):
        await Tortoise.close_connections()

    async def create_tables(self):
        await Tortoise.generate_schemas()

    async def drop_tables(self):
        assert settings.ENV in ("testing", "development")
        for m in self.models:
            await self._connection.execute_query("DROP TABLE " + m._meta.table)
