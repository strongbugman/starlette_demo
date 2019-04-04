import typing

import aioredis

import settings
from .base import Extension


class RedisExtension(Extension):
    def __init__(self):
        super().__init__()
        self.client: typing.Optional[aioredis.Redis] = None

    async def startup(self):
        self.client: aioredis.Redis = await aioredis.create_redis_pool(
            settings.REDIS_URL, timeout=1
        )

    async def shutdown(self):
        self.client.close()
