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
def app():
    from manage import app, app_life

    with app_life():
        yield app


@pytest.fixture()
def client(app):
    yield TestClient(app)


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def db(app):
    from app.extentions import db

    await db.create_tables()
    yield
    await db.drop_tables()


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def cache(app):
    from app.extentions import cache

    await cache.clear()
    yield
    await cache.clear()
