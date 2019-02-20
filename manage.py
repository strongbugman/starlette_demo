#!/usr/bin/env python3
import asyncio
from contextlib import contextmanager
from functools import wraps

from uvicorn import run as _run
import click
from IPython import embed

from app import create_app
from app.extentions import db


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
def init_db():
    with app_life():
        async_run(db.create_tables())


if __name__ == "__main__":
    main()
