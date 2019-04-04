import typing
from asyncio import iscoroutine, sleep, TimeoutError, wait_for

from aio_pika import (
    connect_robust,
    RobustConnection,
    Channel,
    Exchange,
    Queue,
    Message,
    IncomingMessage,
)
from msgpack import dumps, loads
from ant_nest.ant import Ant, CliAnt

import settings
from .base import Extension


class Task:
    def __init__(self, ext: "TaskExtension", func: typing.Callable, name=""):
        self.func: typing.Callable = func
        self.ext: "TaskExtension" = ext
        if name:
            self.name: str = name
        else:
            self.name: str = func.__name__

    async def execute(self, *args, **kwargs) -> None:
        res = self.func(*args, **kwargs)
        if iscoroutine(res):
            await res

    async def delay(self, *args, **kwargs) -> None:
        if settings.ENV == "testing":
            await self.execute(*args, **kwargs)
        else:
            await self.ext.exchange.publish(
                Message(dumps([args, kwargs]), headers={"name": self.name}),
                settings.AMQP_ROUTING_KEY,
            )


class TaskExtension(Extension):
    tasks: typing.Dict[str, Task] = {}

    def __init__(self):
        super().__init__()
        self.connection: typing.Optional[RobustConnection] = None
        self.channel: typing.Optional[Channel] = None
        self.exchange: typing.Optional[Exchange] = None
        self.queue: typing.Optional[Queue] = None
        self.ant: Ant = CliAnt()
        self.ant.concurrent_limit = 20
        self.closed = False

    async def startup(self):
        self.connection = await wait_for(connect_robust(settings.AMQP_URL), timeout=1)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            settings.AMQP_EXCHANGE, durable=True, timeout=1
        )
        self.queue = await self.channel.declare_queue(
            settings.AMQP_QUEUE, durable=True, timeout=1
        )
        await self.queue.bind(self.exchange, settings.AMQP_ROUTING_KEY, timeout=1)

    async def shutdown(self):
        await self.ant.wait_scheduled_coroutines()
        await self.channel.close()
        await self.connection.close()

    def task(self, func: typing.Callable) -> Task:
        t = Task(self, func)
        if t.name in self.tasks:
            raise ValueError(f"Task {t.name} has been declared!")
        self.tasks[t.name] = t
        return t

    async def consume(self, msg: IncomingMessage):
        args, kwargs = loads(msg.body)
        task = self.tasks[msg.headers["name"]]
        try:
            await task.execute(*args, *kwargs)
            await msg.ack()
        except Extension:
            self.logger.exception("Error on task consuming!")
            await msg.reject()

    async def consume_all(self):
        while not self.closed:
            try:
                msg = await self.queue.get(fail=False)
            except TimeoutError:
                continue

            if msg:
                self.ant.schedule_coroutine(self.consume(msg))
            await sleep(5)
