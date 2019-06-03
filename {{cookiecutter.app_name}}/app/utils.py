import typing
from json import JSONDecodeError
import enum

from starlette.requests import Request
from starlette.responses import JSONResponse as _JSONResponse
import ujson

from . import exceptions


def get_sign(func: typing.Callable, *args, **kwargs) -> str:
    return f"{func.__name__}_{args}_{kwargs}".replace(" ", "").replace("'", "")


async def get_json(req: Request) -> typing.Dict:
    try:
        json = getattr(req, "_json", None)
        if json:
            return json
        else:
            json = ujson.loads(await req.body())
            setattr(req, "_json", json)
            return json
    except (JSONDecodeError, ValueError) as e:
        raise exceptions.InvalidJson(str(e)) from e


def parse_integer(num: typing.Union[str, int]) -> int:
    if isinstance(num, str):
        if not num.isdecimal():
            raise exceptions.InvalidId("Filed is not a number!")
        else:
            num = int(num)

    return num


def parse_id(_id: typing.Union[str, int, None]) -> int:
    if not _id:
        raise exceptions.InvalidId("Miss fields!")

    _id = parse_integer(_id)

    if _id < 0:
        raise exceptions.InvalidId("Filed small than zero!")
    else:
        return _id


def parse_paginate(req: Request):
    page = parse_id(req.query_params.get("page", 1))
    count = parse_id(req.query_params.get("count", 20))

    if count > 40:
        raise exceptions.InvalidException("Field is bigger than 40")

    return page, count


class JSONResponse(_JSONResponse):
    def render(self, content: typing.Dict) -> bytes:
        for k in content.keys():
            if isinstance(content[k], enum.Enum):
                content[k] = content[k].name
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")
