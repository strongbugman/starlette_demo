import typing
from dataclasses import dataclass, asdict

from app import extensions as exts


@dataclass
class Cat:
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
        data = asdict(self)
        data.pop("id")

        if self.id != 0:
            await exts.db.update(self.__class__.__name__, data, id=self.id)
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
    async def list(cls) -> typing.List["Cat"]:
        results = await exts.db.fetch(
            f"SELECT {','.join(cls.__annotations__.keys())} FROM cat"
        )
        return [cls(**result) for result in results]


MODELS = {Cat}
