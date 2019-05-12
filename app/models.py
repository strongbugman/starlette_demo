import typing
from datetime import datetime

from pydantic import BaseModel as _BaseModel, ValidationError
from pydantic.error_wrappers import ErrorWrapper

from . import extensions as exts


M = typing.TypeVar("M", bound="Base")


class Base(_BaseModel):
    __db_define__ = """
CREATE TABLE base (
    id      serial PRIMARY KEY NOT NULL,
    created_at timestamp  NOT NULL  DEFAULT current_timestamp,
    updated_at timestamp  NOT NULL  DEFAULT current_timestamp
);"""
    __upsert_columns__ = ""

    id: int = 0
    created_at: typing.Optional[datetime] = None
    updated_at: typing.Optional[datetime] = None

    def __init__(self, **data: typing.Any):
        super().__init__(**data)

        self.validate_all()

    def validate_all(self) -> None:
        errors = self.get_validate_errors()
        if errors:
            raise ValidationError(
                [ErrorWrapper(ValueError(e), loc=f) for f, e in errors.items()]
            )

    def get_validate_errors(self) -> typing.Dict[str, str]:
        errors: typing.Dict[str, str] = {}
        if self.id < 0:
            errors["id"] = "small than zero!"

        return errors

    async def save(self, upsert=False) -> None:
        self.validate_all()

        data = self.dict(exclude={"created_at", "updated_at", "id"})

        if upsert:
            assert self.id == 0
            await exts.db.upsert(self.__class__.__name__, data, self.__upsert_columns__)
        else:
            if self.id != 0:
                await exts.db.update(self.__class__.__name__, data, id=self.id)
            else:
                self.id = await exts.db.insert(self.__class__.__name__, data)

    @classmethod
    async def get(cls: typing.Type[M], _id: int) -> M:
        result = (
            await exts.db.fetch(
                f"SELECT {','.join(cls.__fields__.keys())} FROM {cls.__name__} WHERE id = $1;",
                _id,
            )
        )[0]
        return cls(**result)

    @classmethod
    async def delete(cls, _id: int) -> None:
        await exts.db.execute(f"DELETE FROM {cls.__name__} WHERE id = $1;", _id)

    @classmethod
    @exts.cache.cached()
    async def list(
        cls: typing.Type[M], page: int = 1, count: int = 20
    ) -> typing.List[M]:
        results = await exts.db.fetch(
            f"SELECT {','.join(cls.__fields__.keys())} FROM {cls.__name__} ORDER BY id ASC "
            f"LIMIT $1 OFFSET $2",
            count,
            (page - 1) * count,
        )
        return [cls(**result) for result in results]


class Cat(Base):
    __db_define__ = """
CREATE TABLE cat (
    id      serial PRIMARY KEY NOT NULL,
    name    varchar(32) DEFAULT '' NOT NULL,
    age     integer DEFAULT 0 NOT NULL,
    created_at timestamp  NOT NULL  DEFAULT current_timestamp,
    updated_at timestamp  NOT NULL  DEFAULT current_timestamp
);"""

    name: str
    age: int = 0

    def get_validate_errors(self) -> typing.Dict[str, str]:
        errors = super().get_validate_errors()

        if self.age < 0:
            errors["age"] = "small than zero!"
        if len(self.name) > 32:
            errors["name"] = "length is too long!(Limit to 32)"
        return errors


MODELS = {Cat}


for m_cls in MODELS:
    exts.starchart.schema_generator.add_schema(m_cls.__name__, m_cls.schema())
    exts.starchart.schema_generator.add_schema(
        f"{m_cls.__name__}s",
        {
            "type": "object",
            "properties": {
                "objects": {
                    "type": "array",
                    "items": {"$ref": f"#/components/schemas/{m_cls.__name__}"},
                },
                "page": {"type": "integer"},
                "count": {"type": "integer"},
            },
        },
    )
