import os
import asyncio

import pytest
from starlette.testclient import TestClient


def pytest_configure():
    os.environ["APP_ENV"] = "testing"
    os.environ["DEBUG"] = "True"


@pytest.fixture()
def event_loop():
    yield asyncio.get_event_loop()


@pytest.fixture()
async def app():
    from manage import app

    await app.startup()
    yield app
    await app.shutdown()


@pytest.fixture()
def client(app):
    yield TestClient(app)


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def db(app):
    from app.extensions import db
    from app.models import MODELS

    for M in MODELS:
        await db.create_table(M.__name__, M.__db_define__)
    yield
    for M in MODELS:
        await db.execute(f"DROP TABLE {M.__name__}")


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def cache(app):
    from app.extensions import cache

    await cache.clear()
    yield
    await cache.clear()
