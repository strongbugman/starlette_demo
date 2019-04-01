import typing

from pydantic import BaseModel

from . import extensions as exts


class Cat(BaseModel):
    name: str
    id: int = 0
    age: int = 0

    @classmethod
    def get_db_define(cls) -> str:
        return f"""
        CREATE TABLE {cls.__name__} (
            id      serial PRIMARY KEY,
            name    varchar(32) DEFAULT '',
            age     integer DEFAULT 0
        );
        """

    async def save(self) -> None:
        data = self.dict()
        data.pop("id")

        if self.id != 0:
            await exts.db.update(self.__class__.__name__, data, id=self.id)
        else:
            self.id = await exts.db.insert(self.__class__.__name__, data)

    @classmethod
    async def get(cls, _id) -> "Cat":
        result = (
            await exts.db.fetch(
                f"SELECT {','.join(cls.__annotations__.keys())} FROM cat WHERE id = {exts.db.parse(_id)};"
            )
        )[0]
        return cls(**result)

    @classmethod
    async def delete(cls, _id) -> None:
        await exts.db.execute(
            f"DELETE FROM {cls.__name__} WHERE id = {exts.db.parse(_id)};"
        )

    @classmethod
    @exts.cache.cached()
    async def list(cls, page=1, count=20) -> typing.List["Cat"]:
        results = await exts.db.fetch(
            f"SELECT {','.join(cls.__annotations__.keys())} FROM {cls.__name__} ORDER BY id ASC "
            f"LIMIT {count} OFFSET {(page - 1) * count}"
        )
        return [cls(**result) for result in results]


MODELS = {Cat}
