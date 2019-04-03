from starlette.responses import Response, JSONResponse
from starlette.requests import Request
from pydantic import ValidationError

from . import exceptions


class Handler:
    EXC = Exception

    def handle(self, req: Request, exc: Exception) -> Response:
        return Response(status_code=400)

    @staticmethod
    def error_response(exc: Exception):
        return JSONResponse(
            {"errors": [{"type": exc.__class__.__name__, "detail": str(exc)}]},
            status_code=400,
        )


class NotFoundHandler(Handler):
    EXC = exceptions.NotFound

    def handle(self, req: Request, exc: exceptions.NotFound) -> Response:
        return Response("Resource not found", status_code=404)


class ValidationErrorHandler(Handler):
    EXC = ValidationError

    def handle(self, req: Request, exc: ValidationError) -> JSONResponse:
        return self.error_response(exc)


class InvalidHandler(Handler):
    EXC = exceptions.InvalidException

    def handle(self, req: Request, exc: exceptions.InvalidException) -> JSONResponse:
        return self.error_response(exc)


HANDLERS = {NotFoundHandler(), ValidationErrorHandler(), InvalidHandler()}
