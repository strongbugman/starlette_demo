import typing

from apiman.starlette import Extension as Apiman

import settings
from .base import Extension
from .database import DBExtension
from .cache import CacheExtension
from .redis import RedisExtension

db = DBExtension()
cache = CacheExtension()
redis = RedisExtension()
apiman = Apiman("./docs/template.yml", **settings.APIMAN)

EXTENSIONS: typing.Set[Extension] = {db, cache, redis, apiman}
