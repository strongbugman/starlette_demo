from functools import wraps
import typing
import asyncio

from aiocache import SimpleMemoryCache, RedisCache
from aiocache.base import BaseCache


import settings
from .base import Extension
from app import utils


class CacheExtension(Extension):
    CLIENTS = {"memory": SimpleMemoryCache, "redis": RedisCache}

    def __init__(self):
        super().__init__()
        self.client: BaseCache = self.CLIENTS[settings.CACHE_BACKEND](
            namespace=settings.PROJECT_NAME, **settings.CACHE_KWARGS
        )

    def cached(self, key=None, ttl=10 * 60) -> typing.Callable:
        def decorator(func: typing.Callable) -> typing.Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs) -> typing.Callable:
                nonlocal key

                if not key:
                    key = (
                        self.client.namespace
                        + ":"
                        + utils.get_sign(func, *args, **kwargs)
                    )
                value = await self.client.get(key)
                if value is not None:
                    return value
                else:
                    value = func(*args, **kwargs)
                    if asyncio.iscoroutine(value):
                        value = await value
                    await self.client.set(key, value, ttl=ttl)
                    return value

            return wrapper

        return decorator

    async def clear(self):
        assert settings.ENV in ("testing", "development")
        await self.client.clear()

    async def shutdown(self):
        await self.client.close()
