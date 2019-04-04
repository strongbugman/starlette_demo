import typing

from starchart import Starchart

from .base import Extension
from .database import DBExtension
from .cache import CacheExtension
from .redis import RedisExtension
from .task import TaskExtension

db = DBExtension()
cache = CacheExtension()
redis = RedisExtension()
starchart = Starchart(title="Demo")
task = TaskExtension()

EXTENSIONS: typing.Set[Extension] = {db, cache, redis, starchart, task}
