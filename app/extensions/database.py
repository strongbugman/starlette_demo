import typing

from asyncpg import create_pool, Record
from asyncpg.pool import Pool

import settings
from .base import Extension
from .. import exceptoins


Field = typing.Union[int, float, bool, str, None]


class DBExtension(Extension):
    INSERT_SQL = "INSERT INTO {table:s} ({columns:s}) VALUES ({values:s}) RETURNING id;"
    UPDATE_SQL = "UPDATE {table:s} SET {data:s} WHERE {condition:s};"
    INJECTION_CHARS = ("'", '"', "`", "\\")

    pool: typing.Optional[Pool]

    async def startup(self):
        self.pool = await create_pool(dsn=settings.DB_URL)

    async def shutdown(self):
        await self.pool.close()

    @classmethod
    def parse(cls, value: Field) -> str:
        """Parse value to str for making sql string, eg: False -> '0'
        :return: str
        """
        if isinstance(value, bool):
            return "1" if value else "0"
        elif isinstance(value, str):
            for c in cls.INJECTION_CHARS:
                value = value.replace(c, "\\" + c)
            return "'{:s}'".format(value)
        elif value is None:
            return "NULL"
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            raise ValueError(f"Value {value.__class__}-{value} is not support!")

    async def execute(self, sql: str) -> str:
        self.logger.debug(f"Execute: ```{sql}````")
        async with self.pool.acquire() as conn:
            result = await conn.execute(sql)
            self.logger.debug(f"Result ```{result}````")
        return result

    async def fetch(self, sql: str) -> typing.List[Record]:
        self.logger.debug(f"Fetch: ```{sql}````")
        async with self.pool.acquire() as conn:
            result = await conn.fetch(sql)
            self.logger.debug(f"Result ```{result}````")

        if not result:
            raise exceptoins.NotFound("Not found in PG!")
        return result

    async def insert(self, table: str, data: typing.Dict[str, Field]) -> int:
        keys = data.keys()
        values = data.values()
        sql = self.INSERT_SQL.format(
            table=table,
            columns=", ".join(list(keys)),
            values=", ".join([f"{self.parse(value)}" for value in values]),
        )
        return (await self.fetch(sql))[0]["id"]

    async def update(
        self, table: str, data: typing.Dict[str, Field], **condition: Field
    ):
        sql = self.UPDATE_SQL.format(
            table=table,
            data=", ".join((f"{k}={self.__class__.parse(v)}" for k, v in data.items())),
            condition=", ".join(
                (f"{k}={self.__class__.parse(v)}" for k, v in condition.items())
            ),
        )
        await self.execute(sql)
