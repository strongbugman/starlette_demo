import typing


def get_sign(func: typing.Callable, *args, **kwargs) -> str:
    return f"{func.__name__}_{args}_{kwargs}".replace(" ", "").replace("'", "")
