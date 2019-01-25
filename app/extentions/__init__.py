import typing

from .base import Extension
from .database import DBExtension
from .cache import CacheExtension
from .redis import RedisExtension
from .stagger import Stagger

db = DBExtension()
cache = CacheExtension()
redis = RedisExtension()
stagger = Stagger()

extensions: typing.Set[Extension] = {db, cache, redis, stagger}
