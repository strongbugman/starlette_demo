import typing
import logging

from starlette.applications import Starlette


class Extension:
    def __init__(self):
        self.app: typing.Optional[Starlette] = None
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    def register(self, app: Starlette):
        self.app = app
        app.add_event_handler("startup", self.startup)
        app.add_event_handler("shutdown", self.shutdown)

    def startup(self):
        pass

    def shutdown(self):
        pass
