from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from . import models as m
from .extentions import stagger


class Cat(HTTPEndpoint):
    async def get(self, req: Request):
        """
        summary: Get single cat
        tags:
        - cat
        parameters:
        - name: id
          type: integer
          in: query
          required: True
        responses:
          200:
            description: OK
            schema:
              $ref: '#/definitions/Cat'
          404:
            description: Not found
       """
        cat = await m.Cat.get(id=int(req.query_params.get("id")))
        return JSONResponse(cat.to_dict())

    async def delete(self, req: Request):
        """
        summary: Delete single cat
        tags:
        - cat
        parameters:
        - name: id
          type: integer
          in: query
          required: True
        responses:
          204:
            description: OK
            schema:
              $ref: '#/definitions/Cat'
          404:
            description: Not found
        """
        cat = await m.Cat.get(id=req.query_params.get("id"))
        await cat.delete()
        return JSONResponse(cat.to_dict())


class Cats(HTTPEndpoint):
    async def get(self, req: Request):
        """
        summary: Get all cats
        tags:
        - cats
        parameters:
        - name: id
          type: integer
          in: query
          required: True
        responses:
          200:
            description: OK
        """
        return JSONResponse(await m.Cat.list())

    @stagger.schema_generator.swagger_from("./docs/cats_post.yml")
    async def post(self, req: Request):
        data = await req.json()
        cat = await m.Cat.create(**data)
        return JSONResponse(cat.to_dict())
