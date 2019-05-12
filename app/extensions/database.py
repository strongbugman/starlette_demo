import typing

from asyncpg import create_pool, Record
from asyncpg.pool import Pool

import settings
from .base import Extension
from .. import exceptions


class DBExtension(Extension):
    pool: typing.Optional[Pool]

    async def startup(self):
        self.pool = await create_pool(dsn=settings.DB_URL, timeout=1)
        await self.execute(
            "CREATE OR REPLACE FUNCTION update_row_updated_at() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = now(); RETURN NEW; END; $$ language 'plpgsql';"
        )

    async def shutdown(self):
        await self.pool.close()

    @staticmethod
    def numbsers():
        i = 1
        while True:
            yield i
            i += 1

    async def execute(self, sql: str, *params: typing.Any) -> str:
        assert self.pool
        self.logger.debug(f"Execute: ```{sql}````")
        async with self.pool.acquire() as conn:
            result = await conn.execute(sql, *params)
            self.logger.debug(f"Result ```{result}````")
            return result

    async def fetch(self, sql: str, *params: typing.Any) -> typing.List[Record]:
        assert self.pool
        self.logger.debug(f"Fetch: ```{sql}````")
        async with self.pool.acquire() as conn:
            result = await conn.fetch(sql, *params)
            self.logger.debug(f"Result ```{result}````")

        if not result:
            raise exceptions.NotFound("Not found in PG!")
        return result

    async def insert(self, table: str, data: typing.Dict[str, typing.Any]) -> int:
        sql = "INSERT INTO {table:s} ({keys:}) VALUES ({values:}) RETURNING id;".format(
            table=table,
            keys=", ".join(list(data)),
            values=", ".join([f"${i + 1}" for i in range(len(data))]),
        )
        return (await self.fetch(sql, *data.values()))[0]["id"]

    async def upsert(
        self, table: str, data: typing.Dict[str, typing.Any], upsert_columns: str
    ) -> None:
        numbsers = self.numbsers()
        sql = "INSERT INTO {table:s} ({columns:s}) VALUES ({values:s}) ON CONFLICT ({upsert_columns:s}) DO UPDATE set {pairs:s};".format(
            table=table,
            columns=", ".join(list(data)),
            values=", ".join([f"${next(numbsers)}" for _ in data]),
            upsert_columns=upsert_columns,
            pairs=", ".join(f"{k}=${next(numbsers)}" for k in data),
        )
        await self.execute(sql, *data.values(), *data.values())

    async def update(self, table: str, data: typing.Dict[str, typing.Any], **condition):
        numbsers = self.numbsers()
        sql = "UPDATE {table} SET {data:s} WHERE {condition:s};".format(
            table=table,
            data=", ".join((f"{k}=${next(numbsers)}" for k in data.keys())),
            condition=", ".join((f"{k}=${next(numbsers)}" for k in condition.keys())),
        )
        await self.execute(sql, *data.values(), *condition.values())

    async def create_table(self, name, define):
        await self.execute(define)
        await self.execute(
            f"CREATE TRIGGER update_row_updated_at BEFORE UPDATE ON {name} FOR EACH ROW EXECUTE PROCEDURE  update_row_updated_at();"
        )
