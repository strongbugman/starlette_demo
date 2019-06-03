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
from app.extensions import db


app = create_app()
async_run = asyncio.get_event_loop().run_until_complete


@contextmanager
def app_life():
    async_run(app.startup())
    yield
    async_run(app.shutdown())


@click.group()
def main():
    pass


def cmd(func):
    wrapper = wraps(func)(click.command()(func))

    main.add_command(wrapper)

    return wrapper


@cmd
def shell():
    ctx = {"app": app}
    with app_life():
        embed(user_ns=ctx, using="asyncio")


@cmd
@click.option("--port", default=8000)
def run(port):
    _run(app, port=port)


@cmd
def create_tables():
    with app_life():
        for M in m.MODELS:
            async_run(db.create_table(M.__name__, M.__db_define__))


if __name__ == "__main__":
    main()
