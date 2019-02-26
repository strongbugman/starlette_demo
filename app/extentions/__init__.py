import typing

from starchart import Starchart

from .base import Extension
from .database import DBExtension
from .cache import CacheExtension
from .redis import RedisExtension

db = DBExtension()
cache = CacheExtension()
redis = RedisExtension()
starchart = Starchart(title="Demo")

extensions: typing.Set[Extension] = {db, cache, redis, starchart}