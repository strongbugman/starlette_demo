from starlette.responses import Response
from starlette.requests import Request

from . import exceptoins


class Handler:
    EXC = Exception

    def handle(self, req: Request, exc: Exception):
        pass


class NotFoundHandler(Handler):
    EXC = exceptoins.NotFound

    def handle(self, req: Request, exc: Exception):
        return Response(status_code=404)


HANDLERS = {NotFoundHandler()}
