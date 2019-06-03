import typing

from starlette.routing import Route

from .endpoints import Health, Cat, Cats


ROUTES: typing.List[Route] = [
    Route("/health/", Health, methods=["GET"], name="health"),
    Route("/cat/", Cat, methods=["GET", "DELETE", "PUT"], name="Cat"),
    Route("/cats/", Cats, methods=["GET", "POST"], name="Cats"),
]
