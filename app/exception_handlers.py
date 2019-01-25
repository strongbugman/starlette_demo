from starlette.responses import Response
from starlette.requests import Request
from tortoise.exceptions import DoesNotExist


class Handler:
    EXC = Exception

    def handle(self, req: Request, exc: Exception):
        pass


class NotFoundHandler(Handler):
    EXC = DoesNotExist

    def handle(self, req: Request, exc: Exception):
        return Response(status_code=404)


handlers = {NotFoundHandler()}
