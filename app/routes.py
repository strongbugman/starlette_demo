import typing

from starlette.routing import Route

from .endpoints import Cat, Cats


ROUTES: typing.List[Route] = [
    Route("/cat", Cat, methods=["GET", "DELETE", "PUT"], name="Cat"),
    Route("/cats", Cats, methods=["GET", "POST"], name="Cats"),
]
