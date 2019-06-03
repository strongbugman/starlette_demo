import aioredis

import settings
from .base import Extension


class RedisExtension(aioredis.Redis, Extension):
    def __init__(self):
        aioredis.Redis.__init__(self, None)
        Extension.__init__(self)

    async def startup(self):
        self._pool_or_conn = await aioredis.create_redis_pool(
            settings.REDIS_URL, timeout=1
        )

    async def shutdown(self):
        self.close()
