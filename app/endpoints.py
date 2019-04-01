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
          in: query
          required: True
          schema:
            type: integer
        responses:
          "200":
            description: OK
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Cat'
          "404":
            description: Not found
       """
        cat = await m.Cat.get(int(req.query_params.get("id")))
        return JSONResponse(cat.dict())

    async def delete(self, req: Request):
        """
        summary: Delete single cat
        tags:
        - cat
        parameters:
        - name: id
          in: query
          required: True
          schema:
            type: integer
        responses:
          "204":
            description: OK
          "404":
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
        - name: page
          in: query
          required: False
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: count
          in: query
          required: False
          schema:
            type: integer
            default: 20
            maximum: 40
            minimum: 1
        responses:
          "200":
            description: OK
        """
        cats = await m.Cat.list(
            page=req.query_params.get("page", 1),
            count=req.query_params.get("count", 20),
        )
        return JSONResponse([cat.dict() for cat in cats])

    @starchart.schema_generator.schema_from("./docs/cats_post.yml")
    async def post(self, req: Request):
        data = await req.json()
        cat = m.Cat(**data)
        await cat.save()
        return JSONResponse(cat.dict())
