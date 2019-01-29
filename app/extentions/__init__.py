import typing

from .base import Extension
from .database import DBExtension
from .cache import CacheExtension
from .redis import RedisExtension
from .starchart import Starchart

db = DBExtension()
cache = CacheExtension()
redis = RedisExtension()
starchart = Starchart()

extensions: typing.Set[Extension] = {db, cache, redis, starchart}
