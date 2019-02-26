import typing

from starlette.routing import Route

from .endpoints import Cat, Cats


routes: typing.List[Route] = [
    Route("/cat", Cat, methods=["GET", "DELETE"], name="Cat"),
    Route("/cats", Cats, methods=["GET", "POST"], name="Cats"),
]