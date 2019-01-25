import typing

from starlette.applications import Starlette


class Extension:
    def __init__(self):
        self.app: typing.Optional[Starlette] = None

    def register(self, app: Starlette):
        self.app = app
        app.add_event_handler("startup", self.startup)
        app.add_event_handler("shutdown", self.shutdown)

    def startup(self):
        pass

    def shutdown(self):
        pass
