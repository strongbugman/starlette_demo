#!/usr/bin/env python3
import asyncio
from contextlib import contextmanager
from functools import wraps
import signal

from uvicorn import run as _run
import click
from IPython import embed

from app import create_app
from app import models as m
from app.extensions import db, task


app = create_app()
async_run = asyncio.get_event_loop().run_until_complete


@contextmanager
def app_life():
    async_run(app.router.lifespan.startup())
    yield
    async_run(app.router.lifespan.shutdown())


@click.group()
def main():
    pass


def cmd(func):
    wrapper = wraps(func)(click.command()(func))

    main.add_command(wrapper)

    return wrapper


@cmd
def shell():
    ctx = {"app": app, "async_run": async_run}
    with app_life():
        embed(user_ns=ctx)


@cmd
@click.option("--port", default=8000)
def run(port):
    _run(app, port=port)


@cmd
def task_consume():
    with app_life():

        def _close():
            task.closed = True

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, _close)
        loop.add_signal_handler(signal.SIGTERM, _close)
        print("Consuming tasks...")
        loop.run_until_complete(task.consume_all())


@cmd
def create_tables():
    with app_life():
        for M in m.MODELS:
            async_run(db.execute(M.get_db_define()))


if __name__ == "__main__":
    main()
