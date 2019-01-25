import aioredis

import settings
from .base import Extension


class RedisExtension(Extension):
    def __init__(self):
        super().__init__()
        self.client: aioredis.Redis = aioredis.create_redis_pool(settings.REDIS_URL)

    async def shutdown(self):
        self.client.close()
