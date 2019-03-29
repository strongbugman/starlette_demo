from dataclasses import asdict

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from . import models as m
from .extensions import starchart


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
        definitions:
          Cat:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              age:
                type: integer
          Cats:
            type: object
            properties:
              objects:
                type: array
                items:
                  $ref: "#/definitions/Cat"
       """
        cat = await m.Cat.get(int(req.query_params.get("id")))
        return JSONResponse(asdict(cat))

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
          404:
            description: Not found
        """
        await m.Cat.delete(int(req.query_params.get("id")))
        return Response(status_code=204)


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
        return JSONResponse([asdict(cat) for cat in await m.Cat.list()])

    @starchart.schema_generator.schema_from("./docs/cats_post.yml")
    async def post(self, req: Request):
        data = await req.json()
        cat = m.Cat(**data)
        await cat.save()
        return JSONResponse(asdict(cat))
