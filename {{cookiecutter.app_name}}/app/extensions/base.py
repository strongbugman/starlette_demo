import typing
import logging
import asyncio

from starlette.applications import Starlette


class Extension:
    def __init__(self):
        self.app: typing.Optional[Starlette] = None
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    def init_app(self, app: Starlette):
        self.app = app
        app.add_event_handler("startup", self._startup)
        app.add_event_handler("shutdown", self._shutdown)

    def startup(self):
        pass

    def shutdown(self):
        pass

    async def _startup(self):
        self.logger.debug(f"Startup extension {self.__class__.__name__}")
        res = self.startup()
        if asyncio.iscoroutine(res):
            await res

    async def _shutdown(self):
        self.logger.debug(f"Shutdown extension {self.__class__.__name__}")
        res = self.shutdown()
        if asyncio.iscoroutine(res):
            await res
