import typing

from pydantic import BaseModel as _BaseModel, ValidationError
from pydantic.error_wrappers import ErrorWrapper

from . import extensions as exts


class BaseModel(_BaseModel):
    id: int = 0

    def __init__(self, **data: typing.Any):
        super().__init__(**data)

        self.validate_all()

    def validate_all(self):
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

    @classmethod
    def get_db_define(cls) -> str:
        return f"""
        CREATE TABLE {cls.__name__} (
            id      serial PRIMARY KEY,
        );
        """

    async def save(self) -> None:
        self.validate_all()

        data = self.dict()
        data.pop("id")

        if self.id != 0:
            await exts.db.update(self.__class__.__name__, data, id=self.id)
        else:
            self.id = await exts.db.insert(self.__class__.__name__, data)

    @classmethod
    async def get(cls, _id: int) -> "BaseModel":
        result = (
            await exts.db.fetch(
                f"SELECT {','.join(cls.__fields__.keys())} FROM {cls.__name__} WHERE id = {exts.db.parse(_id)};"
            )
        )[0]
        return cls(**result)

    @classmethod
    async def delete(cls, _id: int) -> None:
        await exts.db.execute(
            f"DELETE FROM {cls.__name__} WHERE id = {exts.db.parse(_id)};"
        )

    @classmethod
    @exts.cache.cached()
    async def list(cls, page: int = 1, count: int = 20) -> typing.List["BaseModel"]:
        results = await exts.db.fetch(
            f"SELECT {','.join(cls.__fields__.keys())} FROM {cls.__name__} ORDER BY id ASC "
            f"LIMIT {count} OFFSET {(page - 1) * count}"
        )
        return [cls(**result) for result in results]


class Cat(BaseModel):
    name: str
    age: int = 0

    def get_validate_errors(self) -> typing.Dict[str, str]:
        errors = super().get_validate_errors()

        if self.age < 0:
            errors["age"] = "small than zero!"
        if len(self.name) > 32:
            errors["name"] = "length is too long!(Limit to 32)"
        return errors

    @classmethod
    def get_db_define(cls) -> str:
        return f"""
        CREATE TABLE {cls.__name__} (
            id      serial PRIMARY KEY,
            name    varchar(32) DEFAULT '',
            age     integer DEFAULT 0
        );
        """


MODELS = {Cat}
