from tortoise.models import Model
from tortoise import fields
from tortoise.queryset import QuerySet

from . import extentions as exts


class Cat(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=10)
    age = fields.SmallIntField(default=0)

    @classmethod
    async def count(cls):
        return await QuerySet(cls).count()

    @classmethod
    @exts.cache.cached(ttl=60)
    async def list(cls):
        cats = []
        async for cat in cls.all():
            cats.append(cat.to_dict())

        return cats

    def to_dict(self):
        return {"id": self.id, "name": self.name, "age": self.age}
