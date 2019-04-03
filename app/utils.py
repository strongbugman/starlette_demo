import typing
from json import JSONDecodeError

from starlette.requests import Request

from . import exceptions


def get_sign(func: typing.Callable, *args, **kwargs) -> str:
    return f"{func.__name__}_{args}_{kwargs}".replace(" ", "").replace("'", "")


async def get_json(req: Request) -> typing.Dict:
    try:
        return await req.json()
    except JSONDecodeError as e:
        raise exceptions.InvalidJson(str(e)) from e


def parse_integer(num: typing.Union[str, int]) -> int:
    if isinstance(num, str):
        if not num.isdecimal():
            raise exceptions.InvalidId("Filed is not a number!")
        else:
            num = int(num)

    return num


def parse_id(_id: typing.Union[str, int, None]) -> int:
    _id = parse_integer(_id)

    if not _id or _id < 0:
        raise exceptions.InvalidId("Filed small than zero!")

    return _id


def parse_paginate(req: Request):
    page = parse_id(req.query_params.get("page", 1))
    count = parse_id(req.query_params.get("count", 20))

    if count > 40:
        raise exceptions.InvalidException("Field is bigger than 40")

    return page, count
